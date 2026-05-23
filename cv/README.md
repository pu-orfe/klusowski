# CV Source

This folder contains the LaTeX source for the CV PDF linked from the homepage.

Files:
- `Klusowski_cv.tex` - main CV source
- `reference_Klusowski.bib` - bibliography entries used by the CV
- `resume.cls` - custom document class required to compile the CV

To update the CV:
1. Edit `Klusowski_cv.tex` and `reference_Klusowski.bib`.
2. Compile from this folder, for example with `latexmk -pdf Klusowski_cv.tex`.
3. Replace `../sites/g/files/toruqf5901/files/documents/Klusowski_cv.pdf` with the generated `Klusowski_cv.pdf`.
4. Commit and push the source changes and updated PDF.
