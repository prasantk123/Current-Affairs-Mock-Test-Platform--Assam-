@echo off
echo Adding GitHub remote...
git remote add origin https://github.com/prasantk123/Current-Affairs-Mock-Test-Platform--Assam-.git

echo Setting main branch...
git branch -M main

echo Pushing to GitHub...
git push -u origin main

echo Done! Your code is now on GitHub.
echo Go to Render and redeploy your service.

pause