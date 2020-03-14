# PyBudget v1.0
----
**Written By:** Joseph Bourque
**Completed On:** 03/14/2020
**Last Upadted:** 03/14/2020
**Contact Email:** indegon1(at)gmail(dot)com

----
A python based weekly (not monthly) budget program which allows the user to manage their budget via json files

----

### Usage
Run the program once using the command `python main.py`. After running you should see a current.json and recurring.json file. 

Entries added to recurring.json are applied automatically every week. Entries added to current.json represent user transactions. 

**Recurring Transaction Format:**
`{"type":"R/W/D", "name":"What am i", "amount":0.00 }`

**Regular Transaction Format:**
`{ "date":"01/01/1970", "type":"R/W/D", "name":"What am i", "amount":0.00 }`

### Transaction Types
* **W** -- Withdrawal: Subtracts funds from the user's total
* **D** -- Deposit: Adds funds to the user's total
* **R** -- Just displays the current total, mainly used for report headers and footers

### Other Options
* **^** -- Applies tax, e.g. **^W** will apply tax to the amount on the withdrawal. This option will be removed during processing and only needs to be applied once.
* **_** -- [WIP] Specifies not to round, right now is just applied once and has to be specified per transaction. I want to add something to the settings on this as well. Not sure when I'm going to get a chance but this will be implemented better at a later date

### Settings
There are a couple of settings located under the settings folder. I'm from the US so I use mm/dd/YYY as a format (fight me). However, I also recognize there are other date formats so I put in the option to change the date format for everything globally. 

**dateFormat** is for formatting all dates except those relating to file names.

**fileFormat** is for formatting names related to file names. This is primarily due to file names not being able to include /. 

**tax rate** This is currently set to 0.0825 and is used by the **^** option. If you have a different tax rate than this feel free to change it in the options.
