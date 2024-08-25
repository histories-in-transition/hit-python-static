function mutateManuscriptLookup(value, data, type, params, component) {
    try {
        let output = value[0]["shelfmark"][0]["value"];
        return `${output}`;
    } catch (error) {
        let output = "no related manuscript"
        return output;
    }
    
}


const colConf = {
    "passages": [
        { title: "ID", field: "hit_id", visible: false },
        { title: "Quote", field: "passage", formatter: "textarea", headerFilter: "input", minWidth: 400 },
        { title: "Work", field: "work", mutator: mutateM2mField, mutatorParams: { labelField: "name" }, headerFilter: "input" },
        { title: "Bible", field: "biblical_references", mutator: mutateSelectField, headerFilter: "input" },
        { title: "Language", field: "language", mutator: mutateSingleSelectField, headerFilter: "list", headerFilterParams: { valuesLookup: true, clearable: true } },
    ],
    "authors": [
        { title: "ID", field: "hit_id", visible: false },
        { title: "Name", field: "name", headerFilter: "input", minWidth: 400 },
        { title: "GND", field: "gnd_url", headerFilter: "input" },
    ],
    "works": [
        { title: "ID", field: "hit_id", visible: false },
        { title: "Title", field: "view_label", headerFilter: "input", minWidth: 400 },
        { title: "Author", field: "author", mutator: mutateM2mField, mutatorParams: { labelField: "name" }, headerFilter: "input" },
    ],
    "manuscripts": [
        { title: "ID", field: "hit_id", visible: false },
        { title: "Name", field: "view_label", headerFilter: "input", minWidth: 400 },
    ],
    "strata": [
        { title: "ID", field: "hit_id", visible: false },
        { title: "Name", field: "view_label", headerFilter: "input", minWidth: 400 },
        { title: "Manuscript", field: "manuscript", mutator: mutateSelectField, headerFilter: "input", minWidth: 400 },
    ],
    "ms_items": [
        { title: "ID", field: "hit_id", visible: false },
        { title: "Name", field: "view_label", headerFilter: "input", minWidth: 400 },
        { title: "Manuscript", field: "manuscript", mutator: mutateManuscriptLookup, headerFilter: "input", minWidth: 400 },
    ],
    "hands": [
        { title: "ID", field: "hit_id", visible: false },
        { title: "Name", field: "view_label", headerFilter: "input", minWidth: 400 },
    ]
}

var table = new Tabulator("#tabulator-table", {
    ajaxURL: dataUrl,
    ajaxResponse: function (url, params, response) {
        let row_data = [...Object.values(response)];
        return row_data;
    },
    height: 600,
    layout: "fitColumns",
    responsiveLayout: "collapse",
    columns: colConf[configKey]
});

table.on("rowClick", function (e, row) {
    var data = row.getData();
    var url = `${data["hit_id"]}.html`
    window.open(url, "_self");
});