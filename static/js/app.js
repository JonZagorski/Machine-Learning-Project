const loadData = d3.csv('NOG.csv').then(data => {
    console.log(data)
    console.log(data[0].Date)
    //const chartResultsData = data['chart']['result'][0];
    //const quoteData = chartResultsData['indicators']['quote'][0];
    return data.map((time, index) => ({
      date: new Date(time * 1000),
      high: quoteData['high'][index],
      low: quoteData['low'][index],
      open: quoteData['open'][index],
      close: quoteData['close'][index],
      volume: quoteData['volume'][index]
    }));
  });
const initialiseChart = data => {
    const margin = { top: 50, right: 50, bottom: 50, left: 50 };
    const width = window.innerWidth - margin.left - margin.right;
    const height = window.innerHeight - margin.top - margin.bottom; 
    // add SVG to the page
    const svg = d3
      .select('#chart')
      .append('svg')
      .attr('width', width + margin['left'] + margin['right'])
      .attr('height', height + margin['top'] + margin['bottom'])
      .call(responsivefy)
      .append('g')
      .attr('transform', `translate(${margin['left']},  ${margin['top']})`);

// find data range
const xMin = d3.min(data, d => {
    return d['date'];
  });
  const xMax = d3.max(data, d => {
    return d['date'];
  });
  const yMin = d3.min(data, d => {
    return d['close'];
  });
  const yMax = d3.max(data, d => {
    return d['close'];
  });
  // scales for the charts
  const xScale = d3
    .scaleTime()
    .domain([xMin, xMax])
    .range([0, width]);
  const yScale = d3
    .scaleLinear()
    .domain([yMin - 5, yMax])
    .range([height, 0])};

// create the axes component
svg
  .append('g')
  .attr('id', 'xAxis')
  .attr('transform', `translate(0, ${height})`)
  .call(d3.axisBottom(xScale));
svg
  .append('g')
  .attr('id', 'yAxis')
  .attr('transform', `translate(${width}, 0)`)
  .call(d3.axisRight(yScale));

// generates close price line chart when called
const line = d3
  .line()
  .x(d => {
    return xScale(d['date']);
  })
  .y(d => {
    return yScale(d['close']);
  });
// Append the path and bind data
svg
 .append('path')
 .data([data])
 .style('fill', 'none')
 .attr('id', 'priceChart')
 .attr('stroke', 'steelblue')
 .attr('stroke-width', '1.5')
 .attr('d', line);

const movingAverage = (data, numberOfPricePoints) => {
    return data.map((row, index, total) => {
      const start = Math.max(0, index - numberOfPricePoints);
      const end = index;
      const subset = total.slice(start, end + 1);
      const sum = subset.reduce((a, b) => {
        return a + b['close'];
      }, 0);
      return {
        date: row['date'],
        average: sum / subset.length
      };
    });
};

// calculates simple moving average over 50 days
const movingAverageData = movingAverage(data, 49);
// generates moving average curve when called
const movingAverageLine = d3
 .line()
 .x(d => {
  return xScale(d['date']);
 })
 .y(d => {
  return yScale(d['average']);
 })
  .curve(d3.curveBasis);
svg
  .append('path')
  .data([movingAverageData])
  .style('fill', 'none')
  .attr('id', 'movingAverageLine')
  .attr('stroke', '#FF8900')
  .attr('d', movingAverageLine);

svg
  .selectAll()
  .data(volData)
  .enter()
  .append('rect')
  .attr('x', d => {
    return xScale(d['date']);
  })
  .attr('y', d => {
    return yVolumeScale(d['volume']);
  })
  .attr('fill', (d, i) => {
    if (i === 0) {
      return '#03a678';
    } else {  
      return volData[i - 1].close > d.close ? '#c0392b' : '#03a678'; 
    }
  })
  .attr('width', 1)
  .attr('height', d => {
    return height - yVolumeScale(d['volume']);
  });

