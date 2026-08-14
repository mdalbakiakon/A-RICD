# Team Collaboration Guide (Git/GitHub — PowerShell)

**Repo Owner:** Md. Al Baki Akon
**Working Branch:** `features/collab-branch` [for collaborators -- this is your working branch]
**Target Branch:** `main` [for collaborators -- do NOT push in main]

This guide will explain to you how our team will collaborate on `features/collab-branch` and how our work eventually gets merged into `main`.

---

## 1. One-Time Setup (Everyone)

Make sure Git is installed and configured:

```powershell
git --version
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

If all good then proceed to cloning. Clone the repository (only once per collaborator):

```powershell
git clone https://github.com/mdalbakiakon/A-RICD.git
cd A-RICD
```

##### REMEMBER: this is codes you will do one single time only!!! after that you always start work from step-2 below.

---

## 2. Getting the Team Branch

Switch to the shared branch and pull the latest changes:

```powershell
git checkout features/collab-branch
git pull origin features/collab-branch
```

---

## 3. Recommended Workflow: Personal Sub-Branch per Contributor

To avoid stepping on each other's changes, each contributor should create their **own sub-branch** off `features/collab-branch` for their task.

```powershell
# Make sure you're up to date first
git checkout features/collab-branch
git pull origin features/collab-branch

# Create your own branch (name it after your task)
git checkout -b feature/collab-branch-<your-name>-<short-task>

"for example: 
git checkout -b feature/collab-branch-baki-RAG_integration"

```

---

## 4. Making Changes

Check what changed:

```powershell
git status
```

Stage and commit changes:

```powershell
git add .
git commit -m "Add: short clear description of the change"
```

> Tip: Commit in small, meaningful chunks rather than one giant commit at the end.

---

## 5. Pushing Your Work

```powershell
git push -u origin feature/collab-branch-<your-name>-<short-task>
```

Then go to GitHub and open a **Pull Request**:

- **Base branch:** `features/collab-branch`
- **Compare branch:** `feature/collab-branch-<your-name>-<short-task>`

Add a short description of what you changed and why, then request a review.

---

## 6. Cleaning Up

After a branch is merged and no longer needed:

```powershell
# Delete local branch
git branch -d feature/collab-branch-<your-name>-<task>

# Delete remote branch
git push origin --delete feature/collab-branch-<your-name>-<task>
```
---

## Golden Rules for the Team

1. **Never push directly to `main`.** Always go through `features/collab-branch` and PRs.
2. **Pull before you start working**, every time.
3. **Commit small and often** easier to review, easier to fix.
4. **One sub-branch per task/feature**, not one branch for everything.
5. **Write clear commit messages** (`Add:`, `Fix:`, `Update:`, `Remove:` prefixes help).
6. **Resolve conflicts locally** before pushing or contact Md. Al Baki Akon. never leave conflict markers in a pushed commit.
7. **Open a PR for every merge**, even into `features/collab-branch` it gives visibility and a review checkpoint.
