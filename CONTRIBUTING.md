# How to contribute
Thank you for your interest in contributing to Yurlungur.

This document describes some points about the contribution process for Yurlungur.


## Workflow

0. `fork` Yurlungur to your GitHub account from [sho7noka/Yurlungur](https://github.com/sho7noka/Yurlungur).
0. `clone` the repository. `git clone git@github.com:your-github-account/yurlungur.git`
  - `git remote add upstream https://github.com/Yurlungur/yurlungur.git`
0. modify your code.
  - `git checkout -b your-branch-name`
    - `your-branch-name` is a name of your modifications, for example,
      `fix/fatal-bugs`, `feature/new-useful-gui` and so on.
  - fix codes, then test them. (if some application installed.)
  - `git commit` them with good commit messages.(check https://github.com/angular/angular.js/blob/master/DEVELOPERS.md#type)
0. `pull` the latest changes form the `dev` branch of the upstream.
  - `git pull upstream dev` or `git pull --rebase upstream dev`.
  - `git commit` them.
  - `git push origin your-branch-name`.
0. make a pull request by template.