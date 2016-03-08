# Contacts Rank

Implement a command-line search tool written in `Ruby`, `python`, `Swift`, or `Javascript`.
Choose the language you know best.

Your script should read in `contacts.json` as its data source
and take one argument, a search query,
and print out an ordered list of `JSON` normalized results,
ranked with the most relevant contacts first.

Example:
```
./contacts-rank.rb z
[
    {
        "name": "Zed",
        "email": "zz@zed.com",
        "phone": "111.111.4444"
    }
]

./contacts-rank.rb zz
[
    {
        "name": "Zed",
        "email": "zz@zed.com",
        "phone": "111.111.4444"
    }
]

./contacts-rank.rb @yahoo
[
    {
        "name": "Jenny J",
        "email": "jj@yahoo.com"
    }
]
```

Write test cases for your script to assert
data is cleaned up,
search hits are filtered,
and results are ranked as you see fit.

Examine the data and rank results intelligently.
Document how your ranking system works and why.

Spend no more than 4 hours.