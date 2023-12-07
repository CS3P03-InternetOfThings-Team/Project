import { getTextFromSpeech } from "../stt.js";
import { calculateEditDistance, wordErrorRate } from "word-error-rate";

let groundTruth = 'Editorial El Comercio. El oro y el crimen. El asesinato de nueve trabajadores en una mina de La Libertad expone la fragilidad de la lucha contra las organizaciones criminales en el país.';
let textIntegratedMicrophone = await getTextFromSpeech({ filename: 'audio/integrated.wav' });
let textM309Microphone = await getTextFromSpeech({ filename: 'audio/m309.wav' });

console.log(`Integrated Microphone WER: ${wordErrorRate(groundTruth, textIntegratedMicrophone)}`);
console.log(`M309 Microphone WER: ${wordErrorRate(groundTruth, textM309Microphone)}`);
