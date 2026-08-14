# Team Collaboration Guide (Git/GitHub — PowerShell)

**Repo Owner:** Md. Al Baki Akon
**Working Branch:** `collab` — for collaborators, this is your working branch
**Target Branch:** `main` — for collaborators, do **NOT** push directly to `main`

This guide explains how our team collaborates on `collab`, and how work eventually gets merged into `main`.

---

## 1. One-Time Setup (Everyone)

Make sure Git is installed and configured:

```powershell
git --version
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

If all good, proceed to cloning. Clone the repository (only once per collaborator):

```powershell
git clone https://github.com/mdalbakiakon/A-RICD.git
cd A-RICD
```

> **REMEMBER:** This is done ONE time only. After that, you always start work from Step 2 below.

---

## 2. Getting the Team Branch

Switch to the shared branch and pull the latest changes:

```powershell
git checkout collab
git pull origin collab
```

---

## 3. Recommended Workflow: Personal Sub-Branch per Contributor

To avoid stepping on each other's changes, each contributor should create their **own sub-branch** off `collab` for their task.

```powershell
# Make sure you're up to date first
git checkout collab
git pull origin collab

# Create your own branch (name it after your task)
git checkout -b collab-<your-name>-<short-task>
```

**Example:**
```powershell
git checkout -b collab-baki-rag_integration
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

> **Tip:** Commit in small, meaningful chunks rather than one giant commit at the end.

---

## 5. Pushing Your Work

```powershell
git push -u origin collab-<your-name>-<short-task>
```

Then go to GitHub and open a **Pull Request**:

- **Base branch:** `collab`
- **Compare branch:** `collab-<your-name>-<short-task>`

Add a short description of what you changed and why, then request a review.

---

## 6. Cleaning Up

After a branch is merged and no longer needed:

```powershell
# Delete local branch
git branch -d collab-<your-name>-<short-task>

# Delete remote branch
git push origin --delete collab-<your-name>-<short-task>
```

---

## Golden Rules for the Team

1. **Never push directly to `main`.** Always go through `collab` and PRs.
2. **Pull before you start working** — every time.
3. **Commit small and often** — easier to review, easier to fix.
4. **One sub-branch per task/feature**, not one branch for everything.
5. **Write clear commit messages** (`Add:`, `Fix:`, `Update:`, `Remove:` prefixes help).
6. **Resolve conflicts locally** before pushing, or contact Md. Al Baki Akon. Never leave conflict markers in a pushed commit.
7. **Open a PR for every merge**, even into `collab` — it gives visibility and a review checkpoint.