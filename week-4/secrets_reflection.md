Reflection:

Think about a codebase you've worked on recently.

1. Think about a substantial change to program behavior that was easy to implement. What were the design decisions changed? Were they secrets?

  I can't remember of when I made a substantial change that was easy.


2. Think about a substantial change to program behavior that was hard to implement. What were the design decisions changed? Should they have been secrets?

  I recently worked on changing a background job that used a CSV as input to process tax refunds and produce a CSV as output for a report of the refunds. The change was to make it also process full refunds. This code was especially difficult to change because the specifics of the CSV file that was inputted were effectively global. The logic for creating the output file was mixed in with the logic processing the tax refunds. Everything was essentially in one big method. My pair and I had to break the code up into separate responsibilities. We had to hide the details of parsing the input CSV file and creating the output CSV file. We had put the logic of calculating the tax refund into a separate module. We also had to separate out the logic for uploading the CSV file to the S3 which was also jammed into the one long function.

  I think the missing modules/secrets were:
  - Parsing the CSV and providing a data structure that was easy to work with.
  - RefundCalculator or something like that whose reponsibility would be to take in the output of the first module and calculate the refund
  - RefundProcessor whose responsibility would have been to interact with the third party payment provider to process the refund
  - ReportCreator which would have created the report showing the successful refunds and the error messages for the unsuccessful ones

  If it was broken up like this, I think the only thing that would have needed to be changed would habe been the RefundCalculator and maybe the RefundProcessor.
