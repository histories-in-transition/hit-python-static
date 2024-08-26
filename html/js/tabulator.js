function mutateManuscriptLookup(value, data, type, params, component) {
    try {
        let output = value[0]["shelfmark"][0]["value"];
        return `${output}`;
    } catch (error) {
        let output = "no related manuscript"
        return output;
    }

}

function handMsLookup(value, data, type, params, component) {
    try {
        let output = value["shelfmark"][0]["value"];
        return `${output}`;
    } catch (error) {
        let output = "no related manuscript"
        return output;
    }
}


function getDistinctRoleValues(data) {
    const roles = data.flatMap(item => item.role);
    const distinctValues = [...new Set(roles.map(role => role.value))];
    return distinctValues.join("; ");
}

function getDistincPlaceValues(data) {
    const roles = data.flatMap(item => item.place);
    const distinctValues = [...new Set(roles.map(role => role.name))];
    return distinctValues.join("; ");
}

function getDistincDateValues(data) {
    const roles = data.flatMap(item => item.dated);
    const distinctValues = [...new Set(roles.map(role => role.label))];
    return distinctValues.join("; ");
}

function getDistincTextValues(data) {
    const roles = data.flatMap(item => item);
    const distinctValues = [...new Set(roles.map(role => role.value))];
    return distinctValues.join("; ");
}


const colConf = {
    "works": [
        { title: "ID", field: "hit_id", visible: false },
        { title: "Title", field: "view_label", headerFilter: "input", minWidth: 400 },
        { title: "Author", field: "author", mutator: mutateM2mField, mutatorParams: { labelField: "name" }, headerFilter: "list",headerFilterFunc: "in", headerFilterParams: {
            valuesLookup: "author", clearable: true, sort: "asc",
            multiselect: true,
        } },
    ],
    "manuscripts": [
        { title: "ID", field: "hit_id", visible: false },
        { title: "Name", field: "view_label", headerFilter: "input", minWidth: 400 },
        { title: "Library", field: "library", mutator: mutateSelectField, headerFilter: "input", minWidth: 400 },
    ],
    "strata": [
        { title: "ID", field: "hit_id", visible: false },
        { title: "Name", field: "view_label", headerFilter: "input", minWidth: 400 },
        {
            title: "Manuscript", field: "manuscript", mutator: mutateSelectField, headerFilter: "list",headerFilterFunc: "in", headerFilterParams: {
                valuesLookup: "manuscript", clearable: true, sort: "asc",
                multiselect: true,
            }, minWidth: 200
        }
    ],
    "ms_items": [
        { title: "ID", field: "hit_id", visible: false },
        { title: "Name", field: "view_label", headerFilter: "input", minWidth: 400 },
        {
            title: "Manuscript", field: "manuscript", mutator: mutateManuscriptLookup,
            headerFilter: "list", headerFilterFunc: "in", headerFilterParams: {
                valuesLookup: "manuscript", clearable: true, sort: "asc",
                multiselect: true,
            }, minWidth: 400
        },
    ],
    "hands": [
        { title: "ID", field: "hit_id", visible: false },
        { title: "Name", field: "view_label", headerFilter: "input", minWidth: 300 },
        {
            title: "Manuscript", field: "manuscript", mutator: handMsLookup, headerFilter: "list", headerFilterFunc: "in", headerFilterParams: {
                valuesLookup: "manuscript", clearable: true, sort: "asc",
                multiselect: true,
            }
        },
        {
            title: "Role", field: "hands_role", mutator: getDistinctRoleValues, headerFilter: "list", headerFilterFunc: "in", headerFilterParams: {
                valuesLookup: "hands_role", clearable: true, sort: "asc",
                multiselect: true,
            }
        },
        {
            title: "Texts", field: "texts", formatter: "textarea", mutator: mutateSelectField, headerFilter: "input", minWidth: 400
        },
        {
            title: "Located in", field: "hands_placed", mutator: getDistincPlaceValues, headerFilter: "list", headerFilterFunc: "in", headerFilterParams: {
                valuesLookup: "hands_placed", clearable: true, sort: "asc",
                multiselect: true,
            }
        },
        {
            title: "Dated", field: "hands_dated", mutator: getDistincDateValues, headerFilter: "list", headerFilterFunc: "in", headerFilterParams: {
                valuesLookup: "hands_dated", clearable: true, sort: "asc",
                multiselect: true,
            }
        }

    ]
}

const groupByConfig = {
    "hands": "manuscript",
    "manuscripts": "library",
    "ms_items": "manuscript",
    "works": "author"
}

let groupBy = getKeyOrDefault(groupByConfig, groupKey)


var table = new Tabulator("#tabulator-table", {
    ajaxURL: dataUrl,
    ajaxResponse: function (url, params, response) {
        let row_data = [...Object.values(response)];
        return row_data;
    },
    height: 600,
    layout: "fitColumns",
    responsiveLayout: "collapse",
    columns: colConf[configKey],
    ...groupBy,
    groupStartOpen:true,
});

table.on("rowClick", function (e, row) {
    var data = row.getData();
    var url = `${data["hit_id"]}.html`
    window.open(url, "_self");
});


table.on("dataLoaded", function (data) {
    var el = document.getElementById("counter1");
    el.innerHTML = `${data.length}`;
    var el = document.getElementById("counter2");
    el.innerHTML = `${data.length}`;
});

table.on("dataFiltered", function (filters, data) {
    var el = document.getElementById("counter1");
    el.innerHTML = `${data.length}`;
}); 