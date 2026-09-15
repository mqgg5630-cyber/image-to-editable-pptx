# local_check.ps1 (repo-specific) - the checks that run on YOUR machine.
# watch.ps1 executes this whenever the agent requests a check (config key
# check_cmd), captures all output to results\status\check_rN_<stamp>.log and
# pushes the verdict back.
#
# This repo = image-to-editable-pptx. The project promise: the deck is a
# REAL editable PowerPoint (native shapes + editable text), not a screenshot
# glued onto a slide. So the local machine verifies exactly that:
#   1. the standard gate (.ps1 ASCII + branch guard + script consistency)
#   2. the fig3 deliverables exist and are not empty
#   3. fig3_mechanism_map.pptx is a well-formed Office package: opens as a
#      zip, has the required parts, 1 slide, >= 220 shapes, >= 80 text runs,
#      >= 1000 editable characters and ZERO pictures (no raster shortcuts)
#   4. fig3_mechanism_map.svg is well-formed XML with >= 80 text nodes
# Exit 0 = passed, anything else = failed.
#
# ASCII-only on purpose (Windows PowerShell 5.1 decodes .ps1 as ANSI/GBK).

$ErrorActionPreference = 'Continue'
Set-Location (Join-Path $PSScriptRoot '..')   # repo root (this file lives in code\)

# full-detail transcript: the scheduled-task host does not reliably pipe the
# nested console output into watch.ps1's $out, so record everything here too
# (results/status/detail_<stamp>.log gets pushed with the verdict)
$__detailDir = Join-Path (Get-Location) 'results\status'
New-Item -ItemType Directory -Force -Path $__detailDir | Out-Null
$__detailLog = Join-Path $__detailDir ('detail_' + (Get-Date -Format 'yyyyMMdd-HHmmss') + '.log')
try { Start-Transcript -LiteralPath $__detailLog | Out-Null } catch { }

$fail = 0

# ---------------------------------------------------------------- 1. gate
if (Test-Path -LiteralPath '.\code\check_all.sh') {
    bash code/check_all.sh
    if ($LASTEXITCODE -ne 0) { Write-Output '[FAIL] gate failed'; $fail = 1 }
}

# ------------------------------------------------- 2. deliverables exist
$pptx = '.\examples\fig3-mechanism-map\fig3_mechanism_map.pptx'
$svg  = '.\examples\fig3-mechanism-map\fig3_mechanism_map.svg'
foreach ($f in @($pptx, $svg)) {
    if (-not (Test-Path -LiteralPath $f)) {
        Write-Output ("[FAIL] missing: {0}" -f $f); $fail = 1
    } elseif ((Get-Item -LiteralPath $f).Length -lt 10KB) {
        Write-Output ("[FAIL] suspiciously small: {0}" -f $f); $fail = 1
    } else {
        Write-Output ("ok: {0} ({1:N0} bytes)" -f $f, (Get-Item -LiteralPath $f).Length)
    }
}

# ------------------------------------------------- 3. pptx is a real deck
if (Test-Path -LiteralPath $pptx) {
    try {
        Add-Type -AssemblyName System.IO.Compression, System.IO.Compression.FileSystem
        $zip = [System.IO.Compression.ZipFile]::OpenRead((Resolve-Path -LiteralPath $pptx).Path)
        $names = @($zip.Entries | ForEach-Object { $_.FullName })

        foreach ($part in @('[Content_Types].xml', 'ppt/presentation.xml', 'ppt/slides/slide1.xml')) {
            if ($names -notcontains $part) {
                Write-Output ("[FAIL] pptx part missing: {0}" -f $part); $fail = 1
            }
        }
        $slideCount = @($names | Where-Object { $_ -match '^ppt/slides/slide\d+\.xml$' }).Count
        Write-Output ("pptx: {0} parts, {1} slide(s)" -f $names.Count, $slideCount)

        $entry = $zip.GetEntry('ppt/slides/slide1.xml')
        $reader = New-Object System.IO.StreamReader($entry.Open())
        $xml = $reader.ReadToEnd()
        $reader.Close()

        $shapes  = [regex]::Matches($xml, '<p:sp>').Count
        $pics    = [regex]::Matches($xml, '<p:pic>').Count
        $runs    = [regex]::Matches($xml, '<a:t>').Count
        $chars   = ([regex]::Matches($xml, '<a:t>(.*?)</a:t>', 'Singleline') | ForEach-Object { $_.Groups[1].Value.Length } | Measure-Object -Sum).Sum
        if ($null -eq $chars) { $chars = 0 }
        Write-Output ("pptx slide1: {0} shapes, {1} pictures, {2} text runs, {3} editable chars" -f $shapes, $pics, $runs, $chars)

        if ($shapes -lt 220) { Write-Output ("[FAIL] expected >= 220 native shapes, got {0}" -f $shapes); $fail = 1 }
        if ($runs   -lt 80)  { Write-Output ("[FAIL] expected >= 80 text runs, got {0}" -f $runs); $fail = 1 }
        if ($chars  -lt 1000){ Write-Output ("[FAIL] expected >= 1000 editable chars, got {0}" -f $chars); $fail = 1 }
        if ($pics   -ne 0)   { Write-Output ("[FAIL] raster shortcut found: {0} <p:pic> (the deck must be native shapes)" -f $pics); $fail = 1 }
        if (($shapes -ge 220) -and ($runs -ge 80) -and ($chars -ge 1000) -and ($pics -eq 0)) {
            Write-Output 'ok: pptx is a fully editable native deck (no raster shortcuts)'
        }
        $zip.Dispose()
    } catch {
        Write-Output ("[FAIL] pptx could not be opened as an Office package: {0}" -f $_.Exception.Message)
        $fail = 1
    }
}

# ------------------------------------------------- 4. svg is well-formed
if (Test-Path -LiteralPath $svg) {
    try {
        $raw = Get-Content -LiteralPath $svg -Raw -Encoding UTF8
        [xml]$null = $raw
        $textNodes = [regex]::Matches($raw, '<text').Count
        Write-Output ("svg: well-formed XML, {0} text nodes" -f $textNodes)
        if ($textNodes -lt 80) { Write-Output ("[FAIL] expected >= 80 svg text nodes, got {0}" -f $textNodes); $fail = 1 }
        else { Write-Output 'ok: svg is well-formed with editable text nodes' }
    } catch {
        Write-Output ("[FAIL] svg is not well-formed XML: {0}" -f $_.Exception.Message)
        $fail = 1
    }
}

try { Stop-Transcript | Out-Null } catch { }
if ($fail -eq 0) { Write-Output '== local checks passed' }
else { Write-Output '== local checks FAILED' }
exit $fail
