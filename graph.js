// Set the dimensions of the canvas / graph

var margin = { top: 30, right: 20, bottom: 170, left: 60 },
  width = 720 -margin.left - margin.right,
  height = 530 - margin.top - margin.bottom;
  
// Set the ranges
var x = d3.scaleTime().range([0, width]);  
var y = d3.scaleLinear().range([height, 0]);
   
// Define the line
var priceline = d3.line()
  .x(function (d) {
     return x(d.rt); 
    })
  .y(function (d) { return y(d.price); });

// Define the axes
var xAxis = d3.axisBottom(x).scale(x)
  .tickFormat(d3.timeFormat("%Y-%m-%d"));

var yAxis = d3.axisLeft(y).scale(y)
  .ticks(5);

// Add the svg canvas
var svg = d3.select("#area1")
  .append("svg")
  .attr("width", width + margin.left + margin.right)
  .attr("height", height + margin.top + margin.bottom)
  .append("g")
  .attr("transform",
    "translate(" + margin.left + "," + margin.top + ")");

svg.append("defs")
  .append("svg:clipPath")
  .attr("id", "clip")
  .append("rect")
  .attr("width", width)
  .attr("height", height);


var stocks ="outputj.json";

// Get the data
d3.json(stocks, function (error, data) {
  data = data.sort();
  data.forEach(function (d) {
    d.rt = Date.parse(d.Date);
    d.price = +d.close;
  });


  var ymax = d3.max(data, function (d) { return d.price; });
    // Scale the range of the data
  x.domain(d3.extent(data, function (d) { return d.rt; }));
  y.domain([0, ymax]);
    

    // Nest the entries by symbol
  var dataNest = d3.nest()
      .key(function (d) { return d.Ticker; })
      .entries(data);

    // set the colour scale
  var color = d3.scaleOrdinal(d3.schemeCategory10);

  legendSpace = width / dataNest.length; // spacing for the legend

  // Loop through each symbol / key
  dataNest.forEach(function (d, i) {
    var series = svg.append("g");

    var firstline =series.append("svg:path")
      .attr("class", "line")
      .attr("clip-path", "url(#clip)")
      .datum(d.values)
      .style("stroke", function () { // Add the colors dynamically
        return d.color = color(d.key);
      })
      .attr("id", 'tag' + d.key.replace(/\s+/g, '')) // assign an ID
      .attr("d", priceline);

    // Add the Legend
    svg.append("text")
      .attr("x", (legendSpace / 2) + i * legendSpace)  // space legend
      .attr("y", height + (margin.bottom / 2) + 5)
      .attr("class", "legend")    // style the legend
      .style("fill", function () {
        // Add the colours dynamically
        return d.color = color(d.key);
    })
    .on("click", function () {
      // Determine if current line is visible 
      var active = d.active ? false : true,
        newOpacity = active ? 0 : 1;
      // Hide or show the elements based on the ID
      d3.select("#tag" + d.key.replace(/\s+/g, ''))
        .transition().duration(100)
        .style("opacity", newOpacity);
      // Update whether or not the elements are active
      d.active = active;
    })
    .text(d.key);


  });

  var extent = [
    [margin.left, margin.top], 
    [width - margin.right, height - margin.top]
    ];
  console.log(extent);
  // Zoom
  var zoomListener = d3.zoom()
    .scaleExtent([1, 10])
    .translateExtent(extent)
    .extent(extent)
    .on("zoom", zoomHandler);

  function zoomHandler() {
    //gX.call(xAxis.scale(d3.event.transform.rescaleX(x)));
    //gY.call(yAxis.scale(d3.event.transform.rescaleY(y)));
    //svg.select(".x.axis").call(xAxis);
    //svg.select(".y.axis").call(yAxis);
    //svg.selectAll(".line")
    //.attr("transform", d3.event.transform);

    x.range([margin.left, width - margin.right]
      .map(
        d => d3.event.transform.applyX(d)
      )
    );


    svg.selectAll(".line")
    .attr('d', priceline);

    svg.select(".x-axis")
    .call(d3.axisBottom(x)
      .tickSizeOuter(0));
    
    //   svg.select('#' + this.id ).attr('d', priceline);
    // })

    // return false;
  //g.attr("transform", d3.event.transform);
  }
  svg.call(zoomListener);

  function hover() {
    var bisect = d3.bisector(d => d.rt).left,
      format = d3.format("+.0%"),
      dateFormat = d3.timeFormat("%Y-%m-%d")
    

    var focus = svg.append("g")
      .attr("class", "focus")
      .style("display", "none");

  // Create the text that travels along the curve of chart
    var focusText = svg
      .append('g')
      .append('text')
      .style("opacity", 0)
      .attr("text-anchor", "left")
      .attr("alignment-baseline", "middle")

    focus.append("line")
      .attr("stroke", "black")
      .attr("stroke-width", 1)
      .attr("y1", -height + margin.top)
      //.attr("y2", -margin.bottom);

    focus.append("circle")
      .attr("class", "circle")
      .attr("r", 5)
      .attr("dy", 5)
      .attr("stroke", "steelblue")
      .attr("fill", "#fff");

    focus.append("text")
      .attr("text-anchor", "middle")
      .attr("dy", ".13em");

    var overlay = svg.append("rect")
      .attr("class", "overlay")
      .attr("width", width)
      .attr("height", height)
      .on("mouseenter", () => focus.style("display", "inline"))
      .on("mouseout", () => focus.style("display", "none"))
      .on("mousemove", mousemove);

    function mousemove() {
      var x0 = x.invert(d3.mouse(this)[0]);
      var i = bisect(data, x0, 1),
      d0 = data[i - 1],
      d1 = data[i],
      d = undefined;
      if(x0 - d0.rt > d1.rt - x0){
        d = d1;
      }
      else{
        d = d0 ;
      }

      focus.select("line")
        .attr("transform", 
          "translate(" + x(d.rt) + "," + height + ")");

      focus.selectAll(".circle")
        .attr("transform", 
          "translate(" + x(d.rt) + "," + y(d.price) + ")");

      focus.select("text")
        .attr("transform", 
          "translate(" + x(d.rt) + "," + (height) + ")")
        .text(dateFormat(d.rt));
    }
  }
  svg.call(hover)
  // Add the X Axis
  var gX = svg.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(0," + height + ")")
    .call(xAxis);

  // Add the Y Axis
  var gY=svg.append("g")
    .attr("class", "y axis")
    .call(yAxis);

  // text label for the x axis
  svg.append("text")             
    .attr("transform",
        "translate(" + (width/2) + " ," + 
                      (height + margin.top + 20) + ")")
    .style("font-size", "18px")
    .style("text-anchor", "middle")
    .text("Stock Symbols");

  // text label for the y axis
  svg.append("text")
    .attr("transform", "rotate(-90)")
    .attr("y", 0 - margin.left)
    .attr("x",0 - (height / 2))
    .attr("dy", "1em")
    .style("font-size", "18px")
    .style("text-anchor", "middle")
    .text("Close Price");  
});


//Chart 2

// Set the ranges
var x = d3.scaleTime().range([0, width]);
var y = d3.scaleLinear().range([height, 0]);

// Define the axes
var xAxis = d3.axisBottom(x).scale(x)
  .ticks(5)
  .tickFormat(d3.timeFormat("%Y-%m-%d"));
  

var yAxis = d3.axisLeft(y).scale(y)
  .ticks(5);

// Define the 1st line
var valueline = d3.line()
  .x(function (d) { return x(d.rt); })
  .y(function (d) { return y(d.p); });

// define the 2nd line
var valueline2 = d3.line()
  .x(function(d) { return x(d.rt); })
  .y(function(d) { return y(d.a); });

// Adds the svg canvas
var chart2 = d3.select("#area2")
  .append("svg")
  .attr("id","predict")
  .attr("width", width + margin.left + margin.right)
  .attr("height", height + margin.top + margin.bottom)
  .append("g")
  .attr("transform",
    "translate(" + margin.left + "," + margin.top + ")");

chart2.append("defs")
  .append("svg:clipPath")
  .attr("id", "clip")
  .append("rect")
  .attr("width", width)
  .attr("height", height);
  

function drawChart()
{
  var Stockdata = "prediction.json";

// Get the data
  d3.json(Stockdata, function (error, data) {
    //data = data.sort(sortByDateAscending);
    console.log(data);
    data.forEach(function (d) {
      d.rt = Date.parse(d.Date);
      d.p = +d.Predicted;
      d.a = +d.Actual;
    });
     // Scale the range of the data
  x.domain(d3.extent(data, function (d) { return d.rt; }));
  
  y.domain([0, d3.max(data, function(d) {
    return Math.max(d.p, d.a); })]);

  // Add the X Axis
  var axisX = chart2.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(0," + height + ")")
    .call(xAxis);

  // Add the Y Axis
  var axisY = chart2.append("g")
    .attr("class", "y axis")
    .call(yAxis);

  //D3 Horizonal Legend //
  var legend_keys = ["Predicted","Actual"] 
  var color = d3.scaleOrdinal(d3.schemeCategory10);
  var dataL = 0;
  var offset = 80;

  var legend4 = chart2.selectAll('#area2')
    .data(legend_keys)
    .enter().append('g')
    .attr("class", "legends4")
    .attr("transform", function (d, i) {
      if (i === 0) {
        dataL = d.length + offset 
        return "translate(0,0)"
      } else { 
        var newdataL = dataL
        dataL +=  d.length + offset
        return "translate(" + (newdataL) + ",0)"
      }
    })

  legend4.append('rect')
    .attr("x", 0)
    .attr("y", 0)
    .attr("width", 10)
    .attr("height", 10)
    .style("fill", function (d, i) {
    return color(i)
  })

  legend4.append('text')
    .attr("x", 20)
    .attr("y", 10)
    .text(function (d, i) {
      return d
    })
    .attr("class", "textselected")
    .style("text-anchor", "start")
    .style("font-size", 15)
 

  // text label for the x axis
  chart2.append("text")             
    .attr("transform",
      "translate(" + (width/2) + " ," + 
          (height + margin.top + 20) + ")")
    .style("font-size", "18px")
    .style("text-anchor", "middle")
    .text("Stock Symbols");

  // text label for the y axis
  chart2.append("text")
    .attr("transform", "rotate(-90)")
    .attr("y", 0 - margin.left)
    .attr("x",0 - (height / 2))
    .attr("dy", "1em")
    .style("font-size", "18px")
    .style("text-anchor", "middle")
    .text("Actual vs Predicted Price");  

  // New select element for allowing the user to select a group!
  var $groupSelector = document.querySelector('.group-select');
  var groupdata = getFilteredData(data, $groupSelector.value);
  groupdata = groupdata.sort(sortByDateAscending);
  console.log(groupdata);
  // // Add the valueline path.
  var line = chart2.append("path")
    .attr("class", "line")
    .attr("clip-path", "url(#clip)")
    .datum(groupdata)
    .attr("id","id")
    .attr("d", valueline)


  chart2.append("path")
    .attr("class", "line")
    .attr("id","id2")
    .attr("clip-path", "url(#clip)")
    .datum(groupdata)
    .style("stroke", "orange")
    .attr("d", valueline2)

  $groupSelector.onchange = function (e) {
    var group = e.target.value;
    var groupData = getFilteredData(data, group);
    updatePoints(groupData);
      //enterPoints(groupData);
    };
  
  //Zoom
  var extent = [
    [margin.left, margin.top], 
    [width - margin.right, height - margin.top]
    ];
  console.log(extent);
  // Zoom
  var zoomListener = d3.zoom()
    .scaleExtent([1, 10])
    .translateExtent(extent)
    .extent(extent)
    .on("zoom", zoomHandler);

  function zoomHandler() {
    //gX.call(xAxis.scale(d3.event.transform.rescaleX(x)));
    //gY.call(yAxis.scale(d3.event.transform.rescaleY(y)));
    //svg.select(".x.axis").call(xAxis);
    //svg.select(".y.axis").call(yAxis);
    //svg.selectAll(".line")
    //.attr("transform", d3.event.transform);

    x.range([margin.left, width - margin.right]
      .map(
        d => d3.event.transform.applyX(d)
      )
    );


    chart2.selectAll("path.line")
    .attr('d', valueline);

    // chart2.selectAll("path.line")
    // .attr('d', valueline2);

    chart2.select(".x-axis")
    .call(d3.axisBottom(x)
      .tickSizeOuter(0));
    
    //   svg.select('#' + this.id ).attr('d', priceline);
    // })

    // return false;
  //g.attr("transform", d3.event.transform);
  }
  chart2.call(zoomListener);

 function hover() {

  var bisect = d3.bisector(d => d.rt).left,
    format = d3.format("+.0%"),
    dateFormat = d3.timeFormat("%Y-%m-%d")
  
  var focuschart = chart2.append("g")
    .attr("class", "focuschart")
    .style("display", "none");
  
  focuschart.append("line")
    .attr("stroke", "black")
    .attr("stroke-width", 1)
    .attr("y1", -height);
    //.attr("y2", -margin.bottom);
  
  focuschart.append("circle")
    .attr("class", "circle")
    .attr("r", 5)
    .attr("dy", 5)
    .attr("stroke", "steelblue")
    .attr("fill", "#fff");
  
  focuschart.append("text")
    .attr("text-anchor", "middle")
    .attr("dy", ".13em");
  
  var overlay = chart2.append("rect")
    .attr("class", "overlay")
    .attr("width", width)
    .attr("height", height)
    .on("mouseover", () => focuschart.style("display", null))
    .on("mouseout", () => focuschart.style("display", "none"))
    .on("mousemove", mousemove);
  
  function mousemove() {
    var x0 = x.invert(d3.mouse(this)[0]);
    var i = bisect(data, x0, 1),
      d0 = data[i - 1],
      d1 = data[i],
      d = undefined;
      if(x0 - d0.rt > d1.rt - x0){
        d = d1;
      }
      else{
        d = d0 ;
      }
      
   focuschart.select("line")
    .attr("transform", 
        "translate(" + x(d.rt) + "," + height + ")");
  
   focuschart.selectAll(".circle")
    .attr("transform", 
    "translate(" + x(d.rt) + "," + y(d.p) + ")");
  
   focuschart.select("text")
    .attr("transform", 
      "translate(" + x(d.rt) + "," + (height) + ")")
    .text(dateFormat(d.rt));
  }
 }
  chart2.call(hover);
 
    
  })
}
drawChart();

function sortByDateAscending(a, b) {
  // Dates will be cast to numbers automatically:
  return a.rt - b.rt;
}
//Get a subset of the data based on the group
function getFilteredData(data, group) {
  return data.filter(function (point) { return point.Ticker === group; });
}

function updatePoints(data) {
  d3.selectAll("#predict > *").html('');
  drawChart();
}
 

// Table 
d3.json('outputj.json', function (error,data) {
  
  function tabulate(data, columns) {
		var table = d3.select('#table').append('table')
		var thead = table.append('thead')
		var	tbody = table.append('tbody');

		// append the header row
		thead.append('tr')
		  .selectAll('th')
		  .data(columns).enter()
		  .append('th')
		    .text(function (column) { return column; });

		// create a row for each object in the data
		var rows = tbody.selectAll('tr')
		  .data(data)
		  .enter()
		  .append('tr');

		// create a cell in each row for each column
		var cells = rows.selectAll('td')
		  .data(function (row) {
		    return columns.map(function (column) {
		      return {column: column, value: row[column]};
		    });
		  })
		  .enter()
		  .append('td')
		    .text(function (d) { return d.value; });

	  return table;
	}

	// render the table(s)
	tabulate(data, ['Date', 'close','Ticker','high','high_low','open','adj_close']); //column table

});
