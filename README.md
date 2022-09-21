# Job Search
Repository for my research on open positions in the field of Electrical Engineering and Software Development.
The objective of this research is to get knowledge on job market to answer the following questions:

1. What are the necessary *skills*?
2. Where are the *main players* in the market?
3. How do these players convey the message in their profiles?
4. How do people in similar job positions behave and convey their message and their brand? Photos, key-words, skills and so on.
5. How to make documents like CVs to propose to these positions?

To answer these questions, the project involves the creation of a database with the jobs' informations like:
- Name of the position
- Enterprise
- City/country
- Assigned level of the position (entry-level, Associate, junior...)
- Number of individuals subscribed
- Key words
- Date of the last actualization
- Link

## Fist stage
The objective is to build a class PostScrapper to get the post information from an URL and store it into a database. This URL is from the Linkedin at first and could expand to other websites later. Also, the URL should be the post's page and not the page of the search result, because it's a more complex problem and will be addressed in further stages.
