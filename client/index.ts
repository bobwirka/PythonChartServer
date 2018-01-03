
/// <reference path="jquery.d.ts" />
/// <reference path="knockout.d.ts" />
/// <reference path="chart.d.ts" />

/**
 * General purpose AJAX exchange function that uses a GET to retrieve a JSON object.
 */
function getJson(url: string , callback: (isSuccess: boolean , result: object)=> any)
{
    $.ajax({
        type     : 'GET',
        url      : url,
        async    : true,

        error    : function(jqXHR , status)
        {
            // Failure.
            callback(false , {'error' : 'AJAX Error: ' + status});
        },
        success  : function (data , status , jqXHR)
        {
            // Success, although the returned object could have 'error'.
            callback(true , JSON.parse(jqXHR.responseText));
        }
    });
}

/**
 * General purpose AJAX exchange function that uses a POST to send and receive JSON objects.
 */
function sendPost(postObject: object , callback: (isSuccess: boolean , result: object)=> any)
{
    $.ajax({
        type     : 'POST',
        url      : 'json-rpc',
        data     : JSON.stringify(postObject),
        dataType : 'json',
        async    : true,

        error    : function(jqXHR , status)
        {
            // Failure.
            callback(false , {'error' : 'AJAX Error: ' + status});
        },
        success  : function (data , status , jqXHR)
        {
            // Success, although the returned object could have 'error'.
            callback(true , JSON.parse(jqXHR.responseText));
        }
    });
}

/******************************************************************************
 *
 * Creates a new chart from the given chart file within the specified <div>.
 *
 ******************************************************************************/

function createNewChart(chartName: string , divName: string , callback: (chart: Chart)=>any)
{
    let chartConfig: Chart.ChartConfiguration;
    let canvasEle:HTMLCanvasElement;
    let context: CanvasRenderingContext2D;
    let newChart: Chart;

    // Sanity check.
    if (chartName === undefined)
        return;
    // Get the chart configuration data.
    getJson('/charts/charts/' + chartName , function(isSuccess: boolean, result: Object)
    {
        if (!isSuccess)
            callback(null);
        chartConfig = <Chart.ChartConfiguration>result;

        canvasEle = <HTMLCanvasElement>document.getElementById(divName);
        context = canvasEle.getContext('2d');
        newChart = new Chart(context, chartConfig);
        callback(newChart);
    })
}

/******************************************************************************
 *
 * Chart view object. Has a drop down to select which chart is displayed.
 *
 ******************************************************************************/

class ChartView
{
    fileNames: KnockoutObservable<string[]> = ko.observable([]);
    selectedName: KnockoutObservable<string> = ko.observable('');

    constructor(fileNames: string[])
    {
        const self: ChartView = this;

        self.selectedName.subscribe(function(newValue: string)
        {
            createNewChart(self.selectedName() , 'chart1' , function(chart: Chart)
            {
                // Nuttin';
            })
        });
        // Apply the object to the single chart element.
        ko.applyBindings(self , $('#chartList')[0]);
        // Apply the file list; this will draw the chart.
        self.fileNames(fileNames);
    }
}
//
let chartView: ChartView;

/******************************************************************************
 *
 * Main
 *
 ******************************************************************************/

$(function()
{
    // Shrink the window (if started as app).
    window.resizeTo(800,500);
    // Get list of available charts.
    getJson('/charts/charts' , function(isSuccess: boolean, obj: Object)
    {
        let fileNames: string[];

        // Return if failure.
        if (!isSuccess)
            return;
        // Cast result as array of strings.
        fileNames = <string[]>obj;
        // Create the view.
        chartView = new ChartView(fileNames);
    });
});