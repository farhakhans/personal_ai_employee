@echo off
echo ================================================================
echo   LINKEDIN CLI POSTER - AI Employee System
echo ================================================================
echo.
echo Usage:
echo   POST: post_linkedin.bat "Your message here"
echo   TEST: post_linkedin.bat --test
echo   POSTS: post_linkedin.bat --posts
echo   HELP: post_linkedin.bat --help
echo.
echo ================================================================
echo.

python post_linkedin_cli.py %*

echo.
echo ================================================================
echo Press any key to exit...
pause >nul
