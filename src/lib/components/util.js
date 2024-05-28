/**
 * @param {number} num
 */
export function round(num) {
	var m = Number((Math.abs(num) * 100).toPrecision(15));
	return (Math.round(m) / 100) * Math.sign(num);
}

export const heatCapOfWater = 4186; // j/l/k

/**
 * @param {number} j
 */
export function tokWh(j) {
	//converts joules to kwh
	return j / 3600e3;
}

/**
 * @param {number} degrees
 */
export function degreesToCompass(degrees) {
	const directions = [
		'North',
		'Northeast',
		'East',
		'Southeast',
		'South',
		'Southwest',
		'West',
		'Northwest'
	];

	const index = Math.round(degrees / 45) % 8;
	return directions[index];
}

/**
 * @param {number} degrees
 */
export function degreesToRoofPitch(degrees) {
	// Convert degrees to radians
	const radians = degrees * (Math.PI / 180);

	// Calculate the rise (tangent of the angle)
	const rise = Math.tan(radians);

	// Typically, the run is expressed as 12 units in roof pitch notation
	const run = 12;

	// Calculate the roof pitch ratio
	const pitch = rise * run;

	if (degrees < 1) return 'Flat';
	if (degrees > 89) return 'Vertical';

	return `${Math.round(pitch)}:${run}`;
}

/**
 * @param {number} v
 * @param {number} pwr
 */
export function vpToR(v, pwr) {
	//converts joules to kwh
	return (v * v) / pwr;
}

/**
 * @param {number} value
 * @param {number} min
 * @param {number} max
 */
export function clamp(value, min, max) {
	if (value < min) return min;
	if (value > max) return max;
	return value;
}

export const formatter = new Intl.DateTimeFormat('en', {
	hour12: true,
	hour: 'numeric',
	minute: '2-digit',
	second: '2-digit'
});

// Month in JavaScript is 0-indexed (January is 0, February is 1, etc),
// but by using 0 as the day it will give us the last day of the prior
// month. So passing in 1 as the month number will return the last day
// of January, not February
/**
 * @param {number} year
 * @param {number} month
 */
export function daysInMonth(year, month) {
	return new Date(year, month + 1, 0).getDate();
}

/**
 * @param {number} liters
 */
export function toGal(liters) {
	return Math.round(liters * 0.264172);
}

/**
 * @param {number} celsius
 */
export function CToF(celsius) {
	let fahrenheit = (celsius * 9) / 5 + 32;

	return Math.round(fahrenheit);
}

/**
 * @param {number} i
 */
export function indexToTime(i) {
	let amPm = 'AM';

	if (i == 0) return 'Midnight';
	// i = i + 1;
	if (i == 12) return 'Noon';

	if (i >= 12) {
		i = i - 12;
		amPm = 'PM';
	}

	return '' + i + amPm;
}

export const months = [
	'January',
	'February',
	'March',
	'April',
	'May',
	'June',
	'July',
	'August',
	'September',
	'October',
	'November',
	'December'
];

// 2022 is the latest tmy available at
// https://developer.nrel.gov/docs/solar/nsrdb/psm3-2-2-tmy-download/
export const year = 2022;

export function getMonthData() {
	return months.map((month, index) => {
		return {
			month: month,
			days: daysInMonth(year, index),
			insolation: 0,
			Edemand: 0,
			Esolar: 0,
			Ecity: 0,
			Epercent: 0,
			savings: 0
		};
	});
}

export const wireGauges = [
	{ id: 1, r: 2.1, text: `8AWG 2.1Ω/km 40A max` },
	{ id: 2, r: 3.35, text: `10AWG 3.35Ω/km 30A max` },
	{ id: 3, r: 5.31, text: `12AWG 5.31Ω/km 20A max` },
	{ id: 4, r: 8.46, text: `14AWG 8.46Ω/km 15A max` }
];

export const moduleTypes = [
	{ id: 0, text: `Standard, 19% eff` },
	{ id: 1, text: `Premium, 21% eff` },
	{ id: 2, text: `Thin Film,  18% eff` }
];

const elementString = `1500W x 120V = 9.6Ω
1650W x 120V = 0.0Ω
2000W x 120V = 7.2Ω
2500W x 120v = 5.76Ω
3000W x 120v = 0.0Ω
2000W x 208V = 21.63Ω
2500W x 208V = 17.3Ω
3000W x 208V = 0.3Ω
3500W x 208V = 12.36Ω
5000W x 208V = 8.65Ω
5500W x 208V = 7.87Ω
6000W x 208V = 7.21Ω
750W x 240V = 0.0Ω
1250W x 240V = 46.08Ω
1500W x 240V = 38.4Ω
2000W x 240V = 28.8Ω
2500W x 240V = 23Ω
3000W x 240V = 19.2Ω
3500W x 240V = 16.46Ω
3800W x 240V = 15.16Ω
4500W x 240V = 12.8Ω
5500W x 240V = 10.47Ω
6000W x 240V = 9.6Ω
4500W x 277V = 17.05Ω
1500W x 277V = 51.15Ω
6000W x 277V = 0.0Ω
3500W x 480V = 65.8Ω
6600W x 480V = 0.0Ω
6000W x 480V = 0.0Ω`;

/**
 * @param {string} str
 */
function parseHeaterElement(str) {
	// Split the string into components
	const parts = str.split(/\s*[x=]\s*/);

	// Extract values and units
	const watts = parseFloat(parts[0]);
	const volts = parseFloat(parts[1]);
	// const resistance = parseFloat(parts[2]);
	const resistance = round(vpToR(volts, watts));

	// Create the object with the extracted values
	const result = {
		label: `${volts}V x ${watts}W ≈ ${resistance}Ω`,
		watts: watts,
		volts: volts,
		resistance: resistance
	};

	return result;
}

function convertElements() {
	const parts = elementString.split(/\n/);

	return parts.map(parseHeaterElement);
}

/**
 * @param {{ resistance: number; }} a
 * @param {{ resistance: number; }} b
 */
function compareElements(a, b) {
	return a.resistance - b.resistance;
}

export const elements = convertElements().sort(compareElements);

export const defaultPrefs = {
	lat: 40.5,
	lng: -104.7,
	selectedModule: null,
	selectedModuleName: null,
	selectedWireId: 2,
	selectedModuleTypeId: 1,
	selectedElement: elements[6],
	Vmp: 38.1,
	Imp: 17.2,
	Voc: 45.2,
	Isc: 18.43,
	panelsPerString: 3,
	parallelStrings: 1,
	azimuth: 180,
	elevation: 40,
	wireLength: 60,
	peakHours: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
	peakPrice: 0.285,
	offPeakPrice: 0.0792,
	losses: 14,
	tankSize: 189, //50 gal
	hotWaterOutTemp: 40,
	hotWaterPerPersonDay: 64, // l/person/day
	personsInHoushold: 4,
	groundTemp: 9,
	energyFactor: 0.91,
	allowNonMpptt: false,
	nonMpptGraph: false,
	bomTotal: 2000,
	yearlySavings: 0
};
