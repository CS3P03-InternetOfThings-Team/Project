import * as sdk from "microsoft-cognitiveservices-speech-sdk";
import { readFile } from "fs/promises";

const API_KEY = "bfd36baa507841fb917dc9d2a7081fb9";
const REGION = "brazilsouth";

let speechConfig = sdk.SpeechConfig.fromSubscription(API_KEY, REGION);
speechConfig.speechRecognitionLanguage = "es-PE";

export const getTextFromSpeech = ({ filename }) => {
  return new Promise(async (resolve) => {
    const audioBuffer = await readFile(filename);
    let audioConfig = sdk.AudioConfig.fromWavFileInput(audioBuffer);
    let speechRecognizer = new sdk.SpeechRecognizer(speechConfig, audioConfig);
    let text = "";
    speechRecognizer.recognized = (s, e) => {
      text += e.result.text + " ";
    };
    speechRecognizer.speechEndDetected = (s, e) => {
      speechRecognizer.stopContinuousRecognitionAsync();
      resolve(text);
    };
    speechRecognizer.startContinuousRecognitionAsync();
  });
};
