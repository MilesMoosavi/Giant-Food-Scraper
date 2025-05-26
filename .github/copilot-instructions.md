<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Giant Food Web Scraper Project Instructions

This is a Python-based web scraping project focused on collecting product data from Giant Food's website for a proof-of-concept mobile shopping application.

## Project Context
- Always refer to PROJECT_CONTEXT.md for understanding the overall project vision and technical approach
- The scraper targets specific HTML selectors documented in PROJECT_CONTEXT.md
- Use requests and BeautifulSoup for web scraping functionality
- Output data should be saved to CSV format in the /data directory

## Code Style Guidelines
- Follow PEP 8 Python coding standards
- Include proper error handling for web requests
- Add informative print statements for debugging and user feedback
- Use meaningful variable names that reflect the data being scraped

## Dependencies
- requests (for HTTP requests)
- beautifulsoup4 (for HTML parsing)
- Add any new dependencies to a requirements.txt file when needed
