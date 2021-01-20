
// Set the dimensions of the canvas / graph
var margin = { top: 30, right: 20, bottom: 70, left: 50 },
  width = 600 - margin.left - margin.right,
  height = 300 - margin.top - margin.bottom;

// Parse the date / time
var parseDate = d3.timeParse("%Y-%m-%dT%H:%M:%S");

// Set the ranges
var x = d3.scaleTime().range([0, width]);
var y = d3.scaleLinear().range([height, 0]);

// Define the line
var priceline = d3.line()
  .x(function (d) { return x(d.date); })
  .y(function (d) { return y(d.price); });

// Adds the svg canvas
var svg = d3.select("#area1")
  .append("svg")
  .attr("width", width + margin.left + margin.right)
  .attr("height", height + margin.top + margin.bottom)
  .append("g")
  .attr("transform",
    "translate(" + margin.left + "," + margin.top + ")");

var stocks = "output.json"
// Get the data
d3.json(stocks, function (error, data) {
  data.forEach(function (d) {
    d.date = parseDate(d.Date);
    d.price = +d.close;
  });
  // Define the axes
  var xAxis = d3.axisBottom(x)
    .tickFormat(d3.timeFormat("%Y-%m-%d"));

  var yAxis = d3.axisLeft(y)
    .ticks(5);

  // Scale the range of the data
  x.domain(d3.extent(data, function (d) { return d.date; }));
  y.domain([0, d3.max(data, function (d) { return d.price; })]);

  // Nest the entries by symbol
  var dataNest = d3.nest()
    .key(function (d) { return d.Ticker; })
    .entries(data);

  // set the colour scale
  var color = d3.scaleOrdinal(d3.schemeCategory10);

  legendSpace = width / dataNest.length; // spacing for the legend

  // Loop through each symbol / key
  dataNest.forEach(function (d, i) {

  var firstline =svg.append("path")
      .attr("class", "line")
      .style("stroke", function () { // Add the colours dynamically
        return d.color = color(d.key);
      })
      .attr("id", 'tag' + d.key.replace(/\s+/g, '')) // assign an ID
      .attr("d", priceline(d.values));

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

  // Add the X Axis
  svg.append("g")
    .attr("class", "axis")
    .attr("transform", "translate(0," + height + ")")
    .call(xAxis);

  // Add the Y Axis
  svg.append("g")
    .attr("class", "axis")
    .call(yAxis);

});

//Chart 2

// Parse the date / time
var parseDate = d3.timeParse("%Y-%m-%dT%H:%M:%S");

// Set the ranges
var x = d3.scaleTime().range([0, width]);
var y = d3.scaleLinear().range([height, 0]);

// Define the axes
var xAxis = d3.axisBottom().scale(x)
  .ticks(5)
  .tickFormat(d3.timeFormat("%Y-%m-%d"))

var yAxis = d3.axisLeft().scale(y)
  .ticks(5);

// Define the 1st line
var valueline = d3.line()
  .x(function (d) { return x(d.date); })
  .y(function (d) { return y(d.close); });
// define the 2nd line
var valueline2 = d3.line()
  .x(function(d) { return x(d.date); })
  .y(function(d) { return y(d.open); });

// Adds the svg canvas
var chart2 = d3.select("#area2")
  .append("svg")
  .attr("width", width + margin.left + margin.right)
  .attr("height", height + margin.top + margin.bottom)
  .append("g")
  .attr("transform",
    "translate(" + margin.left + "," + margin.top + ")");

var Stockdata = "output.json";
// Get the data
d3.json(Stockdata, function (error, data) {
  console.log(data)
  data.forEach(function (d) {
    d.date = parseDate(d.Date);
    d.price = +d.close;
    d.open = +d.open
  
});
  // Scale the range of the data
  x.domain(d3.extent(data, function (d) { return d.date; }));
  y.domain([0, d3.max(data, function(d) {
	  return Math.max(d.close, d.open); })]);
  
  // Add the X Axis
  chart2.append("g")
    .attr("class", "axis")
    .attr("transform", "translate(0," + height + ")")
    .call(xAxis);

  // Add the Y Axis
  chart2.append("g")
    .attr("class", "axis")
    .call(yAxis);

  // Get a subset of the data based on the group
  function getFilteredData(data, group) {
    return data.filter(function (point) { return point.Ticker === group; });
  }
  
  // Helper function to add new points to our data
  function enterPoints(data) {
    console.log(data)
    // Add the points!
    svg.selectAll(".point")
      .data(data)
      .enter().append("path")
      .attr("class", "point")
      .attr('fill', 'red')
      .attr("transform", function (d) { return "translate(" + x(d.date) + "," + y(d.close) + ")"; });
  }

  function updatePoints(data) {

    console.log(data)
    // remove existing lines
    d3.selectAll("#id").remove();
    d3.selectAll("#id1").remove(); 
    d3.selectAll("#id2").remove(); 
    d3.selectAll("#id3").remove(); 

    var line=chart2.append("path")
      .attr("class", "line")
      .attr("id","id1")
      .attr("d", valueline(data)) 

    chart2.append("path")
      .attr("class", "line")
      .attr("id","id3")
      .style("stroke", "red")
      .attr("d", valueline2(data)) 
  }

  // New select element for allowing the user to select a group!
  var $groupSelector = document.querySelector('.group-select');
  var groupData = getFilteredData(data, $groupSelector.value);

  // Enter initial points filtered by default select value set in HTML
  enterPoints(groupData);

  $groupSelector.onchange = function (e) {
    var group = e.target.value;
    var groupData = getFilteredData(data, group);
    console.log(group)
    console.log(groupData)
    updatePoints(groupData);
    enterPoints(groupData);
  };
  // // Add the valueline path.
  var line = chart2.append("path")
  .attr("class", "line")
  .attr("id","id")
  .attr("d", valueline(groupData))

  chart2.append("path")
  .attr("class", "line")
  .attr("id","id2")
  .style("stroke", "red")
  .attr("d", valueline2(groupData))

  });