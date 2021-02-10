// Set the dimensions of the canvas / graph
// var margin = { top: 30, right: 20, bottom: 170, left: 60 },
//   width = 980 -margin.left + margin.right,
//   height = 360 - margin.top + margin.bottom;

var margin = { top: 30, right: 20, bottom: 170, left: 60 },
  width = 700 -margin.left + margin.right,
  height = 360 - margin.top + margin.bottom;
  
// Set the ranges
var x = d3.scaleTime().range([0, width]);  
var y = d3.scaleLinear().range([height, 0]);
   
// Define the line
var priceline = d3.line()
  .x(function (d) { return x(d.rt); })
  .y(function (d) { return y(d.price); });

// Define the axes
var xAxis = d3.axisBottom(x)
  .tickFormat(d3.timeFormat("%Y-%m-%d"));

var yAxis = d3.axisLeft(y)
  .ticks(5);

// Add the svg canvas
var svg = d3.select("#area1")
  .append("svg")
  .attr("width", width + margin.left + margin.right)
  .attr("height", height + margin.top + margin.bottom)
  .append("g")
  .attr("transform",
    "translate(" + margin.left + "," + margin.top + ")");

var stocks ="outputj.json";

// Get the data
d3.json(stocks, function (error, data) {
  data = data.sort();
  data.forEach(function (d) {
    d.rt = Date.parse(d.Date);
    d.price = +d.close;
  });

  
  // Scale the range of the data
x.domain(d3.extent(data, function (d) { return d.rt; }));
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
      //.attr("clip-path", "url(#clip)")
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
// Zoom
var zoom = d3.zoom()
.scaleExtent([1, 8])
.translateExtent([[-100, -100], [width + 90, height + 100]])
.extent([[0, 0], [width, height]])
.on("zoom", zoomed);

function zoomed() {
svg.selectAll(".line")
  .attr("transform", d3.event.transform);
gX.call(xAxis.scale(d3.event.transform.rescaleX(x)));
gY.call(yAxis.scale(d3.event.transform.rescaleY(y)));
}

svg.call(zoom);

function hover() {
var bisect = d3.bisector(d => d.rt).left,
  format = d3.format("+.0%"),
  dateFormat = d3.timeFormat("%Y-%m-%d")

var focus = svg.append("g")
  .attr("class", "focus")
  .style("display", "none");

focus.append("line")
  .attr("stroke", "black")
  .attr("stroke-width", 1)
  .attr("y1", -height + margin.top)
  .attr("y2", -margin.bottom);

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
  .attr("x", margin.left)
  .attr("y", margin.top)
  .attr("width", width - margin.right - margin.left)
  .attr("height", height)
  .on("mouseover", () => focus.style("display", null))
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
  .attr("class", "axis")
  .attr("transform", "translate(0," + height + ")")
  .call(xAxis);

// Add the Y Axis
var gY=svg.append("g")
  .attr("class", "axis")
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

// Parse the date / time
var parseDate = d3.timeParse("%Y-%m-%d");

// Set the ranges
var x = d3.scaleTime().range([0, width]);
var y = d3.scaleLinear().range([height, 0]);

// Define the axes
var xAxis = d3.axisBottom().scale(x)
      .ticks(5)
      .tickFormat(d3.timeFormat("%Y-%m-%d"));
  

var yAxis = d3.axisLeft().scale(y)
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
  .attr("width", width + margin.left + margin.right)
  .attr("height", height + margin.top + margin.bottom)
  .append("g")
  .attr("transform",
    "translate(" + margin.left + "," + margin.top + ")");

var Stockdata = "prediction.json";
// Get the data
d3.json(Stockdata, function (error, data) {
  data = data.sort(sortByDateAscending);
  console.log(data);
  data.forEach(function (d) {
    d.rt = Date.parse(d.Date);
    d.p = +d.Predicted;
    d.a = +d.Actual
  
});
  // Scale the range of the data
  x.domain(d3.extent(data, function (d) { return d.rt; }));
  
  y.domain([0, d3.max(data, function(d) {
    return Math.max(d.p, d.a); })]);
  
  // Add the X Axis
 var axisX = chart2.append("g")
    .attr("class", "axis")
    .attr("transform", "translate(0," + height + ")")
    .call(xAxis);

  // Add the Y Axis
  var axisY = chart2.append("g")
    .attr("class", "axis")
    .call(yAxis);


  // Get a subset of the data based on the group
  function getFilteredData(data, group) {
    return data.filter(function (point) { return point.Ticker === group; });
  }

  function sortByDateAscending(a, b) {
    // Dates will be cast to numbers automatically:
    return a.rt - b.rt;
  }

  // Helper function to add new points to our data
  function enterPoints(data) {
    data = data.sort(sortByDateAscending);
    console.log(data)
    // Add the points!
    svg.selectAll(".point")
      .data(data.sort(function(d){return d}))
      .enter().append("path")
      .attr("class", "point")
      .attr('fill', 'yellow')
      .attr("transform", function (d) { return "translate(" + x(d.rt) + "," + y(d.p) + ")"; });
  }

  function updatePoints(data) {
    data = data.sort(sortByDateAscending);
    //console.log(data)
    // // remove existing lines
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
      .style("stroke", "yellow")
      .attr("d", valueline2(data)) 
  }

  // New select element for allowing the user to select a group!
  var $groupSelector = document.querySelector('.group-select');
  var groupData = getFilteredData(data, $groupSelector.value);

  // Enter initial points filtered by default select value set in HTML
  enterPoints(groupData);

  $groupSelector.onchange = function (e) {
    //data = data.sort(sortByDateAscending);
    var group = e.target.value;
    var groupData = getFilteredData(data, group);
    // console.log(group)
    // console.log(groupData)
    updatePoints(groupData);
    enterPoints(groupData);
  };
  // Zoom
  var zoom = d3.zoom()
  .scaleExtent([1, 8])
  .translateExtent([[-100, -100], [width + 90, height + 100]])
  .extent([[0, 0], [width, height]])
  .on("zoom", zoomed);
 
 function zoomed() {
  chart2.selectAll("path.line")
    .attr("transform", d3.event.transform);
   axisX.call(xAxis.scale(d3.event.transform.rescaleX(x)));
   axisY.call(yAxis.scale(d3.event.transform.rescaleY(y)));
 }
 
 chart2.call(zoom);
 
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
    .attr("y1", -height + margin.top)
    .attr("y2", -margin.bottom);
  
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
    .attr("x", margin.left)
    .attr("y", margin.top)
    .attr("width", width - margin.right - margin.left)
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
 
 
  // // Add the valueline path.
  var line = chart2.append("path")
  .attr("class", "line")
  .attr("id","id")
  .attr("d", valueline(groupData))

  chart2.append("path")
  .attr("class", "line")
  .attr("id","id2")
  .style("stroke", "yellow")
  .attr("d", valueline2(groupData))

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

});

// Table 

