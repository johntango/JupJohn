A progression of data-representation techniques:

flat: Working with lists of records with primitive fields, as in a naive implementation of the relational data model. Top-level dictionary, which is simply a "tuple" of lists, and each list is a mapping. Not surprisingly, quite inefficient, and needs a double loop to find grades on a pset.


flato: Redoing the last version using Python objects. Similar efficiency issues.


dict: Taking the simple step of encoding each appropriate table as a dictionary over its key. Chooses the  [Student ID] |-> [Pset ID] |-> [Points] mapping for grades. Student grades are therefore easily looked up. Grades on a pset need one loop through the items in the grades dictionary.


dicts: To support multiple directions of efficient lookup, use multiple dictionaries to encode one table, mapping to the key type. Student ID to Student Name and Student Name to Student ID. For grades, have two mappings  [Student ID] |-> [Pset ID] |-> [Points] and [Pset ID] |-> [Student ID] |-> [Points]. Student ID from Name gets more efficient -- just one lookup. Grades on a pset gets more efficient. Check quickly if at least one student did the pset (!), by using the second mapping. We get a dictionary of student IDs to points on a particular pset. We need to loop through the students to map student names to points as required. Previously, we had to loop through ALL the grades in the database to find the grades for a particular pset. 
The small downside is that updating the database is a little more work and needs some care to maintain consistency.


obj: Actually, those multiple dictionaries could all be mapping to the same mutable Python objects (dictionaries). We have student objects that are dictionaries with "id" and "name" keys with corresponding id and name values, pset objects with "id" and "points" keys, and grade objects with "student" (id), "pset" (id) and "points" keys. These dictionaries objects are the values in appropriate higher level dictionaries. When you return an object rather than just the id, name, or points, the caller gets more information (how you got to the id, name or points through dictionary lookups).


nested: Instead of just using keys to index into a variety of top-level dictionaries, we can make one field of a dictionary be another dictionary, storing some subset of rows somehow related to the enclosing object. We remove the two grades dictionaries/mappings, and only have student by id, student by name and psets at the top level. However, psets has a grades dictionary inside it. Since students only get grades on psets (and not for anything else), this makes sense. The grade object doesn't change from the obj version, but updating a grade does. Finding grades on a pset has a clean and efficient implementation (no need to check that at least one student did the pset).


cache: To support efficient computation of statistics like averages, add extra fields in objects. psets has an additional key: value pair, i.e., gradesSum: number. Each time a grade is added to the pset the gradesSum value is updated. This means that when we want to compute average score on a pset, we simply divide the gradesSum value by the number of distinct grades. The latter is computed using len(), and len() uses the same trick internally in Python! That is, each time a list or dictionary is updated, len is changed, so it does not require a loop when it is called.
Now assume that we want to be able to:
  (1) enumerate all of a student's grades in increasing pset-ID order.
  (2) enumerate all of a pset's grades in increasing points order.
In the current representation, we have to produce the lists and sort them each time we want to enumerate grades.


multilist: Here's a fancy one: one object may belong to multiple linked lists, supporting different enumeration orders!  We can use sorted lists to avoid sorting at the time of enumeration. The student and pset objects have an extra key: value pair corresponding to a "gradesInOrder" key. Adding a grade has quite a bit of code that shows how to insert into a linked list to maintain a sorted order (of pset IDs). There is similar code to insert into the pset's linked list of grades (sorted by points). Obviously, we do not need to sort when we need to return student grades in order, though we do have to create an appropriate list.
