# CV Source

This folder contains the LaTeX source for the CV PDF linked from the homepage.

Files:
- `Klusowski_cv.tex` - main CV source
- `reference_Klusowski.bib` - bibliography entries used by the CV
- `resume.cls` - custom document class required to compile the CV
- `klusowski-cv.bst` - local BibTeX style derived from the standard `plain` style

The local bibliography style keeps full author lists, paper titles, italicized
journal and conference/book titles, volume and page information, years, and
status notes. It omits conference editor lists, publishers, publication
addresses, and redundant proceedings-series names, and displays dates as years.
Book and chapter citations retain their book titles and relevant edition,
series, and page information. These display choices do not remove any metadata
from `reference_Klusowski.bib`. The original `plain.bst` copyright and copying
notice are preserved in the renamed style file.

The class provides aligned date rows (`\cvEntry` and `\cvTalk`), grouped
institution headings, and continuously numbered `cvPapers` lists. Main sections
create PDF bookmarks and page labels for automatic continuation headings. Use
`latexmk` (or repeat the final LaTeX pass when labels change) to refresh them.

To update the CV:
1. Edit `Klusowski_cv.tex` and `reference_Klusowski.bib`.
2. Compile from this folder with `latexmk -pdf Klusowski_cv.tex`. The build needs
   a LaTeX distribution with BibTeX and the packages loaded by the source; keep
   the local class and bibliography style alongside the `.tex` file. Without
   `latexmk`, run `pdflatex Klusowski_cv.tex`, `bibtex Klusowski_cv`, then
   `pdflatex Klusowski_cv.tex` twice.
3. Replace `../sites/g/files/toruqf5901/files/documents/Klusowski_cv.pdf` with the generated `Klusowski_cv.pdf`.
4. Commit and push the source changes and updated PDF.
