
## Details for creating GMail Filters

### Usage

* create a filter from provided json and save it's definition as json under configured `filters_json_basepath`

```
python3 apply-filter.py config-yaml/apply-filter-config.yaml --from-json data/filters/this_would_be_filter_id_in_name_of_file.json
```

* to apply multiple filter from provided json and save it's definition as json under configured `filters_json_basepath`

```
python3 apply-filter.py config-yaml/apply-filter-config.yaml --from-json data/filters/this_would_be_filter_id_in_name_of_file.json --from-json data/filters/this_would_be_filter_id_in_name_of_file_2.json
```

* to apply a filter from provided json, save filter created and delete the exisiting filter using switch '--remove-older'

```
python3 apply-filter.py config-yaml/apply-filter-config.yaml --from-json data/filters/this_would_be_filter_id_in_name_of_file.json --remove-older
```

---

### JSON Schema for Filter

* Sample JSON for new filter

```
{
    "id": "any-value-if-new-else-it-would-have-if-pre-existing",
    "criteria": {
        "from": "from:(googlegroups.com)"
    },
    "action": {
        "addLabelIds": [
            "newsletters"
        ]
    }
}
```

* full schema

```
{
  "id": string,
  "criteria": {
    "from": string,
    "to": string,
    "subject": string,
    "query": string,
    "negatedQuery": string,
    "hasAttachment": boolean,
    "excludeChats": boolean,
    "size": integer,
    "sizeComparison": string
  },
  "action": {
    "addLabelIds": [
      string
    ],
    "removeLabelIds": [
      string
    ],
    "forward": string
  }
}
```

---
