var data = "clean_data/combined.csv";

function chart(d) {
    var feature = d.feature;
    var trumpdata = feature.properties.votes20_Donald_Trump;
    var bidendata = feature.properties.votes20_Joe_Biden;
    var statename = feature.properties.state;
    console.log(trumpdata);
    console.log(bidendata)
    console.log(statename)
    var margin = {left:20,right:15,top:40,bottom:40};
    var div = d3.select('.paint');
    var svg = div.select("svg");
    width =  svg.attr("width");
    height = svg.attr("height");
    radius = Math.min(width,height)/2;
    var color = d3.scaleOrdinal(["#a83432", "#3275a8"]);
    var data = [{"val": trumpdata, "type": "Trump","state":statename},{"val": bidendata, "type": "Biden","state":statename}];
    console.log(data);
    var g = svg.append("g")
    .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

    var pie = d3.pie()
        .sort(null)
        .value(function(d) { 
            return d.val; 
        });

    var path = d3.arc()
        .outerRadius(radius - 10)
        .innerRadius(0);

    var label = d3.arc()
        .outerRadius(radius - 40)
        .innerRadius(radius - 40);
    
    var arc = g.selectAll(".arc")
        .data(pie(data))
        .enter().append("g")
        .attr("class", "arc");
      
    arc.append("path")
        .attr("d", path)
        .attr("fill", function(d) { return color(d.value); });

 
    var text = arc.append("text")
        .attr("transform", function(d) { return "translate(" + label.centroid(d) + ")"; })
        .attr("dy", "0.35em")
        .style("font-size", "12px")
        .text(function(d) {
             return d.data.val; 
        });

    var title =svg.append("text")
        .attr("x", 60)             
        .attr("y", 15)
        .attr("class", "title")
        .attr("text-anchor", "middle")  
        .style("font-size", "16px") 
        .style("text-decoration", "underline")  
        .attr("d",text)
        .text(function(d,i) {
          return "Election Results"; 
        });
    return div.node();
    
}   
