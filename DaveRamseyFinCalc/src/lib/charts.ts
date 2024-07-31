import * as d3 from 'd3';

export const create_chart = () => {
    // Define the data type
    interface DataPoint {
        date: Date;
        value: number;
    }

    // Sample data
    const data: DataPoint[] = [
        { date: new Date('2024-01-01'), value: 30 },
        { date: new Date('2024-02-01'), value: 50 },
        { date: new Date('2024-03-01'), value: 80 },
        { date: new Date('2024-04-01'), value: 60 },
        { date: new Date('2024-05-01'), value: 90 }
    ];

    // Set dimensions and margins
    const margin = { top: 20, right: 30, bottom: 30, left: 40 };
    const width = 960 - margin.left - margin.right;
    const height = 500 - margin.top - margin.bottom;

    // Create SVG element
    const svg = d3.select('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
    .append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`);

    // Define scales
    const x = d3.scaleTime()
        .domain(d3.extent(data, d => d.date) as [Date, Date])
        .range([0, width]);

    const y = d3.scaleLinear()
        .domain([0, d3.max(data, d => d.value) as number])
        .range([height, 0]);

    // Define the area generator
    const area = d3.area<DataPoint>()
        .x(d => x(d.date))
        .y0(height)
        .y1(d => y(d.value));

    // Add the shaded area
    svg.append('path')
        .datum(data)
        .attr('fill', 'steelblue')
        .attr('d', area as any); // TypeScript issue with the area function type

    // Add x and y axes
    svg.append('g')
        .attr('transform', `translate(0,${height})`)
        .call(d3.axisBottom(x));

    svg.append('g')
        .call(d3.axisLeft(y));

}

