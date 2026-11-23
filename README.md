# StatoGraph

A small Python command-line tool that turns a CSV file into a **bar or pie chart** in a few prompts. Pick a file, choose the columns, and get a chart, with no plotting code needed.

`Python` `pandas` `matplotlib` `tkinter`

## How it works

1. A file dialog opens so you can choose a CSV file.
2. StatoGraph loads it, reports how many rows it read, and lists every column as numeric or text.
3. Choose **bar** or **pie**, then answer the prompts for which columns to use.
4. The chart opens in a matplotlib window.

| Chart | Categories | Values |
|---|---|---|
| **Bar** | Any column | Either the count of each category, or the sum of a numeric column per category (sorted largest first) |
| **Pie** | Any column | Sum of a numeric column per category, shown with percentages |

Input is validated throughout: unknown column names and invalid choices re-prompt, and empty files, non-numeric value columns and missing data give a clear error message instead of a traceback.

## Run it

Needs Python 3.9+ (with `tkinter`, which ships with most Python installs).

```sh
pip install -r requirements.txt
python statograph.py
```

## Example

Given `expenses.csv`:

```text
category,amount
food,10
rent,50
food,5
```

```text
Loaded 3 rows from 'expenses.csv'.

Which chart would you like to create? (bar/pie): bar
Available columns:
 - category (text)
 - amount (numeric)
Enter the column to use for categories: category
Use a numeric column for bar heights? (yes/no): yes
Enter the numeric column for bar heights: amount
```

This opens a bar chart with rent at 50 and food at 15.

## Ideas for next

- Line and scatter charts
- Saving charts to PNG
- Command-line arguments to skip the prompts
