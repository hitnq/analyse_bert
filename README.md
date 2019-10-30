# analyse_bert
anaylse bert in synonyms and abbreviate in QA

# convert data to synonyms single format

#### if using squad data: 
``` 
python get_query_para_sync.py --input_file /path/to/your/squad_data --task_name squad
```
#### if using Natural Question data: 
``` 
python get_query_para_sync.py --input_file /path/to/your/nq_data --output_file /path/to/your/only_short_saving_nq_data --task_name nq
```
#### you will get:
#### if using squad data:
```
./sync_sync_squad.json  ./record_id_squad.txt
```
#### if using Natural Question data: 
```
./sync_sync.json  ./record_id.txt
```
#### Then:
``` 
python convert_sync.py
```
#### Delete duplicate synonyms:
```
python filter_duplicate_examples.py
```


# convert data to synonyms part format

# convert data to synonyms shortcut format
