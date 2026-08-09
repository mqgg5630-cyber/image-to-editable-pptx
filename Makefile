.PHONY: validate test example package

validate:
	python3 scripts/validate_page_ir.py examples/minimal/page_ir.json

test:
	python3 -m unittest discover -s tests -v

example:
	node scripts/compile_page_ir.js examples/minimal/page_ir.json /tmp/image-to-editable-pptx-example.pptx

package:
	python3 scripts/package_skill.py . --outdir /tmp/image-to-editable-pptx-dist
