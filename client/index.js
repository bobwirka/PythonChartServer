/// <reference path="jquery.d.ts" />
/// <reference path="knockout.d.ts" />
/// <reference path="chart.d.ts" />
/**
 * General purpose AJAX exchange function that uses a GET to retrieve a JSON object.
 */
function getJson(url, callback) {
    $.ajax({
        type: 'GET',
        url: url,
        async: true,
        error: function (jqXHR, status) {
            // Failure.
            callback(false, { 'error': 'AJAX Error: ' + status });
        },
        success: function (data, status, jqXHR) {
            // Success, although the returned object could have 'error'.
            callback(true, JSON.parse(jqXHR.responseText));
        }
    });
}
/**
 * General purpose AJAX exchange function that uses a POST to send and receive JSON objects.
 */
function sendPost(postObject, callback) {
    $.ajax({
        type: 'POST',
        url: 'json-rpc',
        data: JSON.stringify(postObject),
        dataType: 'json',
        async: true,
        error: function (jqXHR, status) {
            // Failure.
            callback(false, { 'error': 'AJAX Error: ' + status });
        },
        success: function (data, status, jqXHR) {
            // Success, although the returned object could have 'error'.
            callback(true, JSON.parse(jqXHR.responseText));
        }
    });
}
/******************************************************************************
 *
 * Creates a new chart from the given chart file within the specified <div>.
 *
 ******************************************************************************/
function createNewChart(chartName, divName, callback) {
    var chartConfig;
    var canvasEle;
    var context;
    var newChart;
    // Sanity check.
    if (chartName === undefined)
        return;
    // Get the chart configuration data.
    getJson('/charts/charts/' + chartName, function (isSuccess, result) {
        if (!isSuccess)
            callback(null);
        chartConfig = result;
        canvasEle = document.getElementById(divName);
        context = canvasEle.getContext('2d');
        newChart = new Chart(context, chartConfig);
        callback(newChart);
    });
}
/******************************************************************************
 *
 * Chart view object. Has a drop down to select which chart is displayed.
 *
 ******************************************************************************/
var ChartView = /** @class */ (function () {
    function ChartView(fileNames) {
        this.fileNames = ko.observable([]);
        this.selectedName = ko.observable('');
        var self = this;
        self.selectedName.subscribe(function (newValue) {
            createNewChart(self.selectedName(), 'chart1', function (chart) {
                // Nuttin';
            });
        });
        // Apply the object to the single chart element.
        ko.applyBindings(self, $('#chartList')[0]);
        // Apply the file list; this will draw the chart.
        self.fileNames(fileNames);
    }
    return ChartView;
}());
//
var chartView;
/******************************************************************************
 *
 * Main
 *
 ******************************************************************************/
$(function () {
    // Shrink the window (if started as app).
    window.resizeTo(800, 500);
    // Get list of available charts.
    getJson('/charts/charts', function (isSuccess, obj) {
        var fileNames;
        // Return if failure.
        if (!isSuccess)
            return;
        // Cast result as array of strings.
        fileNames = obj;
        // Create the view.
        chartView = new ChartView(fileNames);
    });
});
//# sourceMappingURL=index.js.map