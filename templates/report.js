 function generateTable() {
             try {
                 var testdetails = document.createElement("div");
                 testdetails.classList.add("chart_div");
                 testdetails.setAttribute("id", "piechart");
                 var dvTable = document.getElementById("testdetails");
                 dvTable.parentNode.replaceChild(testdetails, dvTable);

                 drawChart();

                 var table = document.createElement("Nav");
                 table.classList.add("sidenav");
                 var testdata = ${test_result};


                 //Get the count of columns.

                 var count = testdata.length;
                 var element = document.createElement("c");
                 element.innerHTML = "Test Details Overview";
                 element.onclick = function () {
                     loadpiechart(testdata);
                 };
                 table.appendChild(element);
                 for (var i = 0; i < count; i++) {
                     if (testdata[i].test_status == "Passed") {
                         var element = document.createElement("a");

                         element.innerHTML = testdata[i].test_name;
                         element.onclick = function () {
                             loadpiechart(testdata);
                         };


                     } else {
                         var element = document.createElement("b");
                         element.innerHTML = testdata[i].test_name;
                         element.onclick = function () {
                             loadTestDetails(testdata);
                         };


                     }


                     table.appendChild(element);
                 }

                 var dvTable = document.getElementById("report");
                 dvTable.innerHTML = "";
                 dvTable.appendChild(table);
             }
             catch (e) {

             }
    }

    function loadTestDetails(testdata) {
        try {
            var testdetails = document.createElement("testdetails");
            testdetails.setAttribute("id", "testdetails");
            var count = testdata.length;

            for (var i = 0; i < count; i++) {

                if (testdata[i].test_status != "Passed") {

                    var element = document.createElement("div");
                    element.classList.add("failcard");
                    element.innerHTML = testdata[i].test_name + "----Test Failed";
                    testdetails.appendChild(element);
                    element = document.createElement("div");
                    testdetails.appendChild(element);
                    element = document.createElement("div");
                    element.innerHTML = "Failed Step: " + testdata[i].failed_step;
                    element.classList.add("detail");
                    testdetails.appendChild(element);

                    var element = document.createElement("div");
                    element.classList.add("detail");
                    element.innerHTML = testdata[i].failure_cause;

                    testdetails.appendChild(element);
                    for (j = 0; j < 2; j++) {
                        element = document.createElement("br");
                        testdetails.appendChild(element);
                    }


                }


            }
            var dvTable = document.getElementById("piechart");
            dvTable.parentNode.replaceChild(testdetails, dvTable);
        }
        catch (e)
        {

        }

    }
        function loadpiechart(data)
        {
            try {
                var testdetails = document.createElement("div");

                testdetails.setAttribute("id", "piechart");
                testdetails.classList.add("chart_div");
                var dvTable = document.getElementById("testdetails");
                dvTable.parentNode.replaceChild(testdetails, dvTable);

                drawChart();
            } catch (e)
            {

            }
        }
         google.charts.load('current', {'packages':['corechart']});
         google.charts.setOnLoadCallback(drawChart);
function drawChart() {
    try {

        var data = google.visualization.arrayToDataTable([
            ['Test Result ', 'Number of tests'],

            ['Failed', ${failed_count}], ['Passed', ${passed_count}]
        ]);

        // add a title and set the width and height of the chart
        var options = {
            'title': 'Test Result', 'width': "100%", 'height': "100%", pieHole: 0.4, colors: ["#CC5500", "#32CD32"]

        };

        // Display the chart inside the <div> element with id="piechart"
        var chart = new google.visualization.PieChart(document.getElementById('piechart'));
        chart.draw(data, options);
    }catch (e) {

    }


}