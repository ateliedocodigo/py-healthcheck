# Contributing to Project

## Development workflow with Git

### Fork, Branching, Commits, and Pull Request

1. [Fork a repo](http://help.github.com/fork-a-repo/) **ateliedocodigo/py-healthcheck**.

2. Clone the **py-healthcheck** project to your local machine (**username** - your Github user account name.):
```
$ git clone git@github.com:USERNAME/py-healthcheck.git
```
3. Configure remotes:
```
$ cd py-healthcheck
$ git remote add upstream git@github.com:ateliedocodigo/py-healthcheck.git
```
4. Create a branch for new check:
```
$ git checkout -b my-new-check
```
5. Develop on **my-new-check** branch only, but **Do not merge my-new-check branch to the your develop (as it should stay equal to upstream develop)!!**

6. Commit changes to **my-new-check** branch:
```
$ git add .
$ git commit -m "commit message"
```

6.1. Update `CHANGELOG.md`

Example: 
```
### Next Release

* My changes closes #1
```

7. Push branch to GitHub, to allow your mentor to review your code:
```
$ git push origin my-new-check
```
8. Repeat steps 5-7 till development is complete.

9. Fetch upstream changes that were done by other contributors:
```
$ git fetch upstream
```
10. Update local develop branch:
```
$ git checkout develop
$ git pull upstream develop
```

ATTENTION: any time you lost of track of your code - launch "gitk --all" in source folder, UI application come up that will show all branches and history in pretty view, [explanation](http://lostechies.com/joshuaflanagan/2010/09/03/use-gitk-to-understand-git/).

11. Rebase **my-new-check** branch on top of the upstream master:
```
$ git checkout my-new-check
$ git rebase master
```
12. In the process of the **rebase**, it may discover conflicts. In that case it will stop and allow you to fix the conflicts. After fixing conflicts, use **git add .** to update the index with those contents, and then just run:
```
$ git rebase --continue
```
13. Push branch to GitHub (with all your final changes and actual code of project):
We forcing changes to your issue branch(our sand box) is not common branch, and rebasing means recreation of commits so no way to push without force. NEVER force to common branch.
```
$ git push origin my-new-check --force
```

14. Created build for testing and send it to any mentor for testing.

15. Only after all testing is done - Send a [Pull Request](http://help.github.com/send-pull-requests/).
Attention: Please recheck that in your pull request you send only your changes, and no other changes!!
Check it by command:
```
git diff my-new-check upstream/develop
```
More detailed information you can find on [Git-rebase (Manual Page)](http://kernel.org/pub/software/scm/git/docs/git-rebase.html) and [Rebasing](http://git-scm.com/book/en/v2/Git-Branching-Rebasing).

## Running tests

Install dependencies
```
$ pip install tox
```

Run tests!
```
$ tox
```
