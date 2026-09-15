# local_check.ps1 (template) - the repo-specific checks that run on YOUR
# machine. watch.ps1 executes this whenever the agent requests a check
# (config key check_cmd), captures all output to
# results\status\check_rN_<stamp>.log and pushes the verdict back.
#
# Exit 0 = passed, anything else = failed. Edit freely - this file belongs to
# the repo, the installer only creates it when it is missing.
#
# Ideas for real checks (pick what fits the repo):
#   - deliverable files exist and have sane sizes
#   - open an Office file via COM to prove it is not corrupt
#   - python -c "import torch; assert torch.cuda.is_available()"  (GPU smoke test)
#   - run a script from code\ and compare its output
#
# ASCII-only on purpose (Windows PowerShell 5.1 decodes .ps1 as ANSI/GBK).

$ErrorActionPreference = 'Continue'
Set-Location (Join-Path $PSScriptRoot '..')   # repo root (this file lives in code\)

$fail = 0

# 1. the standard gate (.ps1 ASCII + branch guard + script consistency)
#    (forward slashes on purpose: this also runs under the scheduled task,
#     where bash may eat backslashes)
if (Test-Path -LiteralPath '.\code\check_all.sh') {
    bash code/check_all.sh
    if ($LASTEXITCODE -ne 0) { Write-Host '[FAIL] gate failed' -ForegroundColor Red; $fail = 1 }
}

# 2. example: the deliverable must exist and not be empty
# if (-not (Test-Path '.\deliverable\final.pptx')) {
#     Write-Host '[FAIL] deliverable\final.pptx missing' -ForegroundColor Red; $fail = 1
# }


# 2. this repo's deliverables must exist and not be empty
foreach ($f in @(
    'examples\fig3-mechanism-map\fig3_mechanism_map.pptx',
    'examples\fig3-mechanism-map\fig3_mechanism_map.svg'
)) {
    if (-not (Test-Path -LiteralPath ('.\' + $f))) {
        Write-Host ("[FAIL] missing: {0}" -f $f) -ForegroundColor Red; $fail = 1
    } elseif ((Get-Item -LiteralPath ('.\' + $f)).Length -lt 10KB) {
        Write-Host ("[FAIL] suspiciously small: {0}" -f $f) -ForegroundColor Red; $fail = 1
    } else {
        Write-Host ("ok: {0}" -f $f) -ForegroundColor Green
    }
}

# 3. add your own checks here ...

if ($fail -eq 0) { Write-Host '== local checks passed' -ForegroundColor Green }
exit $fail
