%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Medium Length Professional CV
% LaTeX Class
% Version 3.0 (December 17, 2022)
%
% This template has been downloaded from:
% http://www.LaTeXTemplates.com
%
% Original header:
% Copyright (C) 2010 by Trey Hunner
%
% Copying and distribution of this file, with or without modification,
% are permitted in any medium without royalty provided the copyright
% notice and this notice are preserved. This file is offered as-is,
% without any warranty.
%
% Created by Trey Hunner and modified by www.LaTeXTemplates.com
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Layout helpers for the academic CV. Keep content in Klusowski_cv.tex.
\ProvidesClass{resume}[2026/10/08 v4.0 Academic CV class]
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}
\ProcessOptions\relax
\LoadClass{article}

\RequirePackage[T1]{fontenc}
\RequirePackage{geometry,array,tabularx,xparse,etoolbox,enumitem,needspace}
\RequirePackage{longtable,multicol,fancyhdr,xcolor}
\geometry{top=0.75in,bottom=0.7in,left=0.75in,right=0.75in,
  headheight=13pt,headsep=12pt,footskip=25pt}
\setlength{\parindent}{0pt}
\setlength{\parskip}{3pt}
\setlength{\emergencystretch}{1.5em}
\clubpenalty=10000
\widowpenalty=10000
\displaywidowpenalty=10000
\raggedbottom
\setlist[itemize]{leftmargin=1.1em,itemsep=2pt,parsep=0pt,topsep=3pt,partopsep=0pt}

\pagestyle{fancy}
\fancyhf{}
% Page labels make continuation headings follow the section at the top of a page.
\newcommand{\cvSectionHeaders}{}
\newcommand{\cvCheckContinuation}[2]{%
  \ifnum\getpagerefnumber{cv-start-#1}<\value{page}%
    \ifnum\getpagerefnumber{cv-end-#1}<\value{page}\else
      \def\cvHeaderText{#2 (continued)}%
    \fi
  \fi
}
\newcommand{\cvRunningTitle}{%
  \begingroup\def\cvHeaderText{Curriculum vitae}%
  \cvSectionHeaders\cvHeaderText\endgroup
}
\fancyhead[L]{\small\color{black!55}Jason M. Klusowski}
\fancyhead[R]{\small\color{black!55}\cvRunningTitle}
\fancyfoot[L]{\footnotesize\color{black!55}Updated \today}
\fancyfoot[R]{\footnotesize\color{black!55}Klusowski\enspace\textperiodcentered\enspace page \thepage}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}
\fancypagestyle{firstpage}{\fancyhead{}}

\newcommand{\cvName}{}
\newcommand{\name}[1]{\renewcommand{\cvName}{#1}}
\newcommand{\cvContact}{}
\newcommand{\address}[1]{\gappto\cvContact{#1}}
\AtBeginDocument{%
  \thispagestyle{firstpage}%
  \begin{center}
    {\LARGE\bfseries\MakeUppercase{\cvName}}\par
    \vspace{3pt}
    {\small\cvContact}
  \end{center}
  \vspace{-5pt}%
}

\newcounter{cvSection}
\newenvironment{rSection}[1]{%
  \par\addvspace{13pt}%
  \Needspace{5\baselineskip}%
  \markright{#1}%
  \stepcounter{cvSection}\pdfbookmark[0]{#1}{cv-section-\thecvSection}%
  \label{cv-start-\thecvSection}%
  \begingroup\edef\cvRegister{\endgroup
    \noexpand\g@addto@macro\noexpand\cvSectionHeaders{%
      \noexpand\cvCheckContinuation{\thecvSection}{\unexpanded{#1}}}}\cvRegister
  {\normalsize\bfseries\MakeUppercase{#1}\par}%
  \nobreak\vspace{2pt}\hrule\nobreak\vspace{5pt}%
  \begin{list}{}{\setlength{\leftmargin}{0pt}\setlength{\rightmargin}{0pt}%
    \setlength{\topsep}{0pt}\setlength{\parsep}{3pt}\setlength{\itemsep}{0pt}}%
  \item[]%
}{\end{list}\label{cv-end-\thecvSection}\par}

\newcommand{\cvGroupHeader}[1]{%
  \par\addvspace{8pt}\Needspace{5\baselineskip}%
  {\bfseries #1\par}\nopagebreak\vspace{1pt}%
}
\newcommand{\cvTypeHeader}[1]{%
  \par\addvspace{4pt}\Needspace{4\baselineskip}%
  {\itshape #1\par}\nopagebreak%
}

% One institutional heading can introduce several appointments or courses.
\newcommand{\cvInstitution}[2]{%
  \par\addvspace{6pt}\Needspace{5\baselineskip}%
  \begin{tabularx}{\linewidth}{@{}>{\raggedright\arraybackslash}X@{\hspace{1em}}r@{}}
    \textbf{#1} & {\small #2}
  \end{tabularx}\par\nopagebreak%
}

% Date column and wrapping text column; keep each short entry on one page.
\newcommand{\cvEntry}[3]{%
  \par\addvspace{3pt}\noindent
  \begin{minipage}{\linewidth}
    \setlength{\parskip}{0pt}%
    \begin{tabularx}{\linewidth}{@{}>{\raggedright\arraybackslash}p{1.22in}@{\hspace{1em}}>{\raggedright\arraybackslash}X@{}}
      {\small #1} & #2\IfBlankF{#3}{\newline {\small #3}}
    \end{tabularx}
  \end{minipage}\par
}
\newcommand{\cvTalk}[3]{%
  \par\addvspace{2pt}\noindent
  \begin{minipage}{\linewidth}
    \begin{tabularx}{\linewidth}{@{}>{\raggedright\arraybackslash}p{1.08in}@{\hspace{1em}}>{\raggedright\arraybackslash}X@{}}
      {\small #1} & \textbf{#2}\IfBlankF{#3}{\enspace\textperiodcentered\enspace{\small #3}}
    \end{tabularx}
  \end{minipage}\par
}

% A single sequence makes every research paper uniquely identifiable.
\newlist{cvPaperList}{enumerate}{1}
\setlist[cvPaperList]{label=\arabic*.,leftmargin=1.9em,labelsep=0.5em,
  itemsep=4pt,parsep=2pt,topsep=2pt,partopsep=0pt,
  beginpenalty=10000,midpenalty=100,endpenalty=0}
\newcounter{cvPaperNumber}
\newenvironment{cvPapers}{%
  \begin{cvPaperList}\setcounter{cvPaperListi}{\value{cvPaperNumber}}%
  \raggedright\interlinepenalty=10000
  \clubpenalty=10000\widowpenalty=10000
}{\setcounter{cvPaperNumber}{\value{cvPaperListi}}\end{cvPaperList}}

% Awards, grants, and service groups share the same restrained heading style.
\NewDocumentEnvironment{rSubsection}{m m m m +b}{%
  \par\addvspace{5pt}%
  \IfBlankF{#1#2#3}{%
    \Needspace{4\baselineskip}%
    \noindent\begin{minipage}{\linewidth}
      \setlength{\parskip}{1pt}%
      \IfBlankTF{#2}{\textbf{#1}\par}{%
        \begin{tabularx}{\linewidth}{@{}>{\raggedright\arraybackslash}X@{\hspace{1em}}>{\raggedleft\arraybackslash}p{1.35in}@{}}
          \textbf{#1} & #2
        \end{tabularx}\par
      }%
      \IfBlankF{#3}{%
        \IfBlankTF{#4}{{\itshape #3\par}}{%
          \begin{tabularx}{\linewidth}{@{}>{\raggedright\arraybackslash}X@{\hspace{1em}}>{\raggedleft\arraybackslash}p{1.35in}@{}}
            \parbox[t]{\linewidth}{\itshape #3} & {\itshape #4}
          \end{tabularx}\par
        }%
      }%
    \end{minipage}\par\nopagebreak
  }%
  \IfBlankF{#5}{\begin{itemize}[label=\textperiodcentered]#5\end{itemize}}%
}{\par}
