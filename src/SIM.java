import java.io.*;
import java.util.*;

public class SIM {
    public static void main(String[] args) throws IOException {
        String originalFile = "original.txt";
        String compressedFile = "compressed.txt";
        compression(originalFile);
        decompression(compressedFile);
    }

    private static void compression(String originalFile) throws IOException {
        ArrayList<String> originalList = readFile(originalFile);
        HashMap<String ,String> dictionary = createDictionary(originalList);
        List<String> compressedInstructions = compressionList(originalList);
        writeCompressedFile(compressedInstructions, dictionary);
    }

    private static ArrayList<String> readFile(String filePath) throws FileNotFoundException {

        File originalFile = new File(filePath);
        Scanner scanner = new Scanner(originalFile);
        ArrayList<String> originalList = new ArrayList<>();
        while (scanner.hasNextLine()) {
            String entry = scanner.nextLine();
            originalList.add(entry.trim());
        }
        scanner.close();
        return originalList;
    }

    private static HashMap<String, String> createDictionary(ArrayList<String> originalList){
        HashMap<String, Integer> entryFrequency = new LinkedHashMap<>();
        for (String entry: originalList){
            if(entryFrequency.containsKey(entry)){
                entryFrequency.put(entry,entryFrequency.get(entry)+1);
            }
            else{
                entryFrequency.put(entry,1);
            }
        }
        ArrayList<Integer> frequencies = new ArrayList<>(entryFrequency.values());
        frequencies.sort(Collections.reverseOrder());
        return selectDictionaryEntries(entryFrequency, frequencies);
    }

    private static HashMap<String, String> selectDictionaryEntries(HashMap<String,Integer> entryFrequency, ArrayList<Integer> frequencies){
        HashMap<String, String> dictionaryEntries = new LinkedHashMap<>();
        for (int i=0; i<8; i++) {
            String binaryValue = Integer.toBinaryString(i);
            if (binaryValue.length()==1) {
                binaryValue = "00"+binaryValue;
            }
            if (binaryValue.length()==2) {
                binaryValue = "0"+binaryValue;
            }
            for(Map.Entry<String, Integer> entry : entryFrequency.entrySet()){
                String key = entry.getKey();
                Integer value = entry.getValue();
                if (value.equals(frequencies.get(i))) {
                    dictionaryEntries.put(key, binaryValue);
                    entryFrequency.remove(key);
                    break;
                }
            }
        }
        return dictionaryEntries;
    }

    private static ArrayList<String> compressionList(ArrayList<String> originalList){
        ArrayList<String> compressedInstructions = new ArrayList<>();

        HashMap<String ,String> dictionary = createDictionary(originalList);

        checkConsecutiveRepetitions (originalList);

        for (String entry: originalList){
            String instructionToCompress = entry.trim().substring(0,32);

            int consecutiveRepetitions= Integer.parseInt((entry.substring(entry.length()-1)));

            String compressedInstruction = beneficialCompressionFormat(instructionToCompress,dictionary);

            compressedInstructions.add(compressedInstruction);

            if (consecutiveRepetitions>0){
                String rleCompressedInstruction = rleCompression(consecutiveRepetitions);

                if(rleCompressedInstruction.length() <= compressedInstruction.length()){
                    compressedInstructions.add(rleCompressedInstruction);
                }
                else{
                    for (int i=0; i<consecutiveRepetitions;i++) {
                        compressedInstructions.add(compressedInstruction);
                    }
                }
            }
        }
        return compressedInstructions;
    }

    private static void checkConsecutiveRepetitions (ArrayList<String> inputInstructions){
        for (int instructionLine=0; instructionLine<inputInstructions.size(); instructionLine++) {
            int repeatedCount = 0;
            String instruction = inputInstructions.get(instructionLine);
            for (int i=1; i<5;i++) {
                if ((instructionLine + 1) < inputInstructions.size()) {
                    String nextInstruction = inputInstructions.get(instructionLine + 1);
                    if (instruction.equals(nextInstruction)) {
                        repeatedCount += 1;
                        inputInstructions.remove(instructionLine + 1);
                    }
                }
            }
            String newI = instruction + " - " + repeatedCount;
            inputInstructions.set(instructionLine, newI);
        }
    }

    private static String beneficialCompressionFormat(String instruction, HashMap<String, String> dictionary){
        ArrayList<String> compressionFormats = new ArrayList<>();

        compressionFormats.add(bitMaskBasedCompression(instruction, dictionary));
        compressionFormats.add(oneBitMismatchCompression(instruction, dictionary));
        compressionFormats.add(twoBitConsecutiveMismatchCompression(instruction, dictionary));
        compressionFormats.add(twoBitMismatchCompression(instruction, dictionary));
        compressionFormats.add(directMatchingCompression(instruction, dictionary));
        compressionFormats.add(originalBinariesCompression(instruction));

        String beneficialCompression = compressionFormats.get(5);
        for (String format: compressionFormats) {
            if (!format.equals("NA") && (format.length() < beneficialCompression.length())){
                beneficialCompression = format;
            }
        }
        return beneficialCompression;
    }

    private static String rleCompression(int rleCount){
        String countToBinary = Integer.toBinaryString(rleCount-1);
        countToBinary=("00" + countToBinary).substring(countToBinary.length());
        return "000"+ countToBinary;
    }

    private static String bitMaskBasedCompression(String instruction, HashMap<String, String> dictionary){
        String compressedInstruction = "NA";
        for (Map.Entry<String, String> dictionaryEntry : dictionary.entrySet()){

            String xorResult = xorOperation(instruction,dictionaryEntry.getKey());
            int startingLocation=xorResult.indexOf("1");

            if ((startingLocation!=-1) && (startingLocation <= xorResult.length()-4)) {
                if (((startingLocation + 4) == xorResult.length()) || (!xorResult.substring(startingLocation + 4).contains("1"))) {
                    String bitMask = xorResult.substring(startingLocation, startingLocation + 4);
                    String startingBit = Integer.toBinaryString(startingLocation);
                    startingBit=("00000" + startingBit).substring(startingBit.length());
                    String dictionaryIndex = dictionaryEntry.getValue();

                    compressedInstruction = "001" + startingBit + bitMask + dictionaryIndex;
                    break;
                }
            }
        }
        return compressedInstruction;
    }

    private static String oneBitMismatchCompression(String instruction, HashMap<String, String> dictionary){
        String compressedInstruction = "NA";
        for (Map.Entry<String, String> dictionaryEntry : dictionary.entrySet()) {
            String xorResult = xorOperation(instruction, dictionaryEntry.getKey());
            if (xorResult.chars().filter(ch -> ch == '1').count() == 1) {
                String mismatchLocation = Integer.toBinaryString(xorResult.indexOf("1"));
                mismatchLocation=("00000" + mismatchLocation).substring(mismatchLocation.length());
                String dictionaryIndex = dictionaryEntry.getValue();

                compressedInstruction = "010" + mismatchLocation+ dictionaryIndex;
                break;
            }
        }
        return compressedInstruction;
    }

    private static String twoBitConsecutiveMismatchCompression(String instruction, HashMap<String, String> dictionary){
        String compressedInstruction = "NA";
        for (Map.Entry<String, String> dictionaryEntry : dictionary.entrySet()) {
            String xorResult = xorOperation(instruction, dictionaryEntry.getKey());
            int consecutiveMisMatch = xorResult.indexOf("11");
            if(consecutiveMisMatch != -1 && xorResult.indexOf("1",consecutiveMisMatch+2)==-1){
                String mismatchLocation = Integer.toBinaryString(consecutiveMisMatch);
                mismatchLocation = ("00000" + mismatchLocation).substring(mismatchLocation.length());
                String dictionaryIndex = dictionaryEntry.getValue();

                compressedInstruction = "011" + mismatchLocation + dictionaryIndex;
                break;
            }
        }
        return compressedInstruction;
    }

    private static String twoBitMismatchCompression(String instruction, HashMap<String, String> dictionary){
        String compressedInstruction = "NA";
        for (Map.Entry<String, String> dictionaryEntry : dictionary.entrySet()) {
            String xorResult = xorOperation(instruction, dictionaryEntry.getKey());
            if (xorResult.chars().filter(ch -> ch == '1').count() ==2) {
                int firstMismatch = xorResult.indexOf("1");
                String mismatchLocation1 = Integer.toBinaryString(firstMismatch);
                mismatchLocation1 = ("00000" + mismatchLocation1).substring(mismatchLocation1.length());
                int secondmismatch = xorResult.indexOf("1", firstMismatch+1);
                String mismatchLocation2 = Integer.toBinaryString(secondmismatch);
                mismatchLocation2 = ("00000" + mismatchLocation2).substring(mismatchLocation2.length());
                String dictionaryIndex = dictionaryEntry.getValue();

                compressedInstruction = "100" + mismatchLocation1 + mismatchLocation2 + dictionaryIndex;
                break;
            }
        }

        return compressedInstruction;
    }

    private static String directMatchingCompression(String instruction, HashMap<String, String> dictionary){
        String compressedInstruction = "NA";
        for(Map.Entry<String, String> entry : dictionary.entrySet()){
            if (instruction.equals(entry.getKey())){
                compressedInstruction="101"+entry.getValue();
            }
        }
        return compressedInstruction;
    }

    private static String originalBinariesCompression(String instruction){

        return "110" + instruction;
    }

    private static String xorOperation (String stringA, String stringB){
        StringBuilder answer = new StringBuilder();
        if (stringA.length()==stringB.length()) {
            for (int i = 0; i < stringA.length(); i++) {
                answer.append(stringA.charAt(i) ^ stringB.charAt(i));
            }
            return answer.toString();
        }
        else{
            return "stringA and stringB are not equal in length";
        }

    }

    public static void writeCompressedFile(List<String> compressedInstructionList, Map<String, String> dictionary) throws IOException {
        StringBuilder compressedText = new StringBuilder();

        for (String compressedInstruction : compressedInstructionList){
            compressedText.append(compressedInstruction);
        }
        int addOnes = compressedText.length()%32;
        if (addOnes>0){
            compressedText.append("1".repeat(32-addOnes));
        }

        FileWriter compressedFile = new FileWriter("cout.txt");
        BufferedWriter buffer = new BufferedWriter(compressedFile);

        for (int i = 0; i < compressedText.length(); i+=32){
            buffer.write(compressedText.substring(i,i+32));
            buffer.newLine();
        }

        buffer.write("xxxx");
        buffer.newLine();

        for(String dictionaryEntry:  dictionary.keySet()){
            buffer.write(dictionaryEntry);
            buffer.newLine();
        }

        buffer.close();
        compressedFile.close();

    }

    // Decompression

    private static void decompression (String compressedFile) throws IOException {
        ArrayList<String> decompressedCodeAndDictionary = readFileToDecompress(compressedFile);
        HashMap<String,String> dictionary= dictionaryToDecompress(decompressedCodeAndDictionary);
        ArrayList<String> compressedList = compressedCodeToList(decompressedCodeAndDictionary);
        ArrayList<String> decompressedList = decompressedList(compressedList, dictionary);
        writeDecompressedFile(decompressedList);
    }

    private static ArrayList<String> readFileToDecompress(String filePath) throws FileNotFoundException {
        File compressedFile = new File(filePath);
        Scanner scanner = new Scanner(compressedFile);
        ArrayList<String> decompressedCodeAndDictionary = new ArrayList<>();
        while (scanner.hasNextLine()) {
            String line = scanner.nextLine();
            decompressedCodeAndDictionary.add(line.trim());
        }
        scanner.close();
        return decompressedCodeAndDictionary;
    }

    private static HashMap<String,String> dictionaryToDecompress(ArrayList<String> decompressedCodeAndDictionary){
        HashMap<String,String> dictionary = new LinkedHashMap<>();
        int seperationMarker = decompressedCodeAndDictionary.indexOf("xxxx");
        for (int i=1;i<9;i++){
            String dictionaryIndex = Integer.toBinaryString(i-1);
            dictionaryIndex =("000" + dictionaryIndex).substring(dictionaryIndex.length());
            dictionary.put(dictionaryIndex, decompressedCodeAndDictionary.get(seperationMarker+i));
        }
        return dictionary;
    }

    private static ArrayList<String> compressedCodeToList (ArrayList<String> decompressedCodeAndDictionary) {
        StringBuilder compressedCodeString = new StringBuilder();
        ArrayList<String> compressedList = new ArrayList<>();
        int seperationMarker = decompressedCodeAndDictionary.indexOf("xxxx");
        for (int i = 0; i < seperationMarker; i++) {
            compressedCodeString.append(decompressedCodeAndDictionary.get(i));
        }

        for (int i = 0; i < compressedCodeString.length()-3; i++) {
            String header = compressedCodeString.substring(i, i + 3);
            switch (header) {
                case "000":
                    compressedList.add(compressedCodeString.substring(i, i + 5));
                    i += 4;
                    break;
                case "001":
                    compressedList.add(compressedCodeString.substring(i, i + 15));
                    i += 14;
                    break;
                case "010" , "011":
                    compressedList.add(compressedCodeString.substring(i, i + 11));
                    i += 10;
                    break;
                case "100":
                    compressedList.add(compressedCodeString.substring(i, i + 16));
                    i += 15;
                    break;
                case "101":
                    compressedList.add(compressedCodeString.substring(i, i + 6));
                    i += 5;
                    break;
                case "110":
                    try {
                        compressedList.add(compressedCodeString.substring(i, i + 35));
                        i += 34;
                    } catch (StringIndexOutOfBoundsException ex) {
                        break;
                    }
                    break;
            }
        }
        return compressedList;
    }

     private static ArrayList<String> decompressedList (ArrayList<String> compressedList, HashMap<String,String> dictionary){
        ArrayList<String> decompressedList = new ArrayList<>();
        for (String compressedPattern: compressedList){
            String header = compressedPattern.substring(0, 3);

            switch (header) {
                case "000" -> {
                    String repeatedInstruction = decompressedList.get(decompressedList.size() - 1);
                    int repetitiveCount = Integer.parseInt(compressedPattern.substring(3, 5), 2) + 1;
                    for (int i = 0; i < repetitiveCount; i++) {
                        decompressedList.add(repeatedInstruction);
                    }
                }
                case "001" -> decompressedList.add(bitMaskBasedDecompression(compressedPattern, dictionary));
                case "010" -> decompressedList.add(oneBitMismatchDecompression(compressedPattern, dictionary));
                case "011" -> decompressedList.add(twoBitConsecutiveMismatchDecompression(compressedPattern, dictionary));
                case "100" -> decompressedList.add(twoBitMismatchDecompression(compressedPattern, dictionary));
                case "101" -> decompressedList.add(directMatchingDecompression(compressedPattern, dictionary));
                case "110" -> decompressedList.add(originalBinariesDecompression(compressedPattern));
            }
        }
        return decompressedList;
    }

    private static String bitMaskBasedDecompression(String compressedPattern, HashMap<String, String> dictionary){
        String instruction="";
        String bitMask ="";
        int startingLocation = Integer.parseInt(compressedPattern.substring(3,8),2);
        String dictionaryEntry = dictionary.get(compressedPattern.substring(12));
        bitMask=  ("0".repeat(startingLocation)) + compressedPattern.substring(8,12) + ("0".repeat(28 - startingLocation));
        instruction = xorOperation(dictionaryEntry,bitMask);
        return instruction;
    }

    private static String oneBitMismatchDecompression(String compressedPattern, HashMap<String, String> dictionary){
        int misMatchLocation = Integer.parseInt(compressedPattern.substring(3,8),2);
        StringBuilder dictionaryEntry = new StringBuilder(dictionary.get(compressedPattern.substring(8)));
        char misMatchBit = dictionaryEntry.charAt(misMatchLocation);
        dictionaryEntry.setCharAt(misMatchLocation,changeBit(misMatchBit));
        return dictionaryEntry.toString();
    }

    private static String twoBitConsecutiveMismatchDecompression(String compressedPattern, HashMap<String, String> dictionary){
        int misMatchLocation = Integer.parseInt(compressedPattern.substring(3,8),2);
        StringBuilder dictionaryEntry = new StringBuilder(dictionary.get(compressedPattern.substring(8)));
        char misMatchBit1 = dictionaryEntry.charAt(misMatchLocation);
        char misMatchBit2 = dictionaryEntry.charAt(misMatchLocation+1);
        dictionaryEntry.setCharAt(misMatchLocation,changeBit(misMatchBit1));
        dictionaryEntry.setCharAt(misMatchLocation+1,changeBit(misMatchBit2));
        return dictionaryEntry.toString();
    }

    private static String twoBitMismatchDecompression(String compressedPattern, HashMap<String, String> dictionary){
        int misMatchLocation1 = Integer.parseInt(compressedPattern.substring(3,8),2);
        int misMatchLocation2 = Integer.parseInt(compressedPattern.substring(8,13),2);
        StringBuilder dictionaryEntry = new StringBuilder(dictionary.get(compressedPattern.substring(13)));
        char misMatchBit1 = dictionaryEntry.charAt(misMatchLocation1);
        char misMatchBit2 = dictionaryEntry.charAt(misMatchLocation2);
        dictionaryEntry.setCharAt(misMatchLocation1,changeBit(misMatchBit1));
        dictionaryEntry.setCharAt(misMatchLocation2,changeBit(misMatchBit2));
        return dictionaryEntry.toString();
    }

    private static String directMatchingDecompression(String compressedPattern, HashMap<String, String> dictionary){
        String instruction="";
        String dictionaryIndex = compressedPattern.substring(3);
        instruction = dictionary.get(dictionaryIndex);
        return instruction;
    }

    private static String originalBinariesDecompression(String compressedPattern){
        return compressedPattern.substring(3);
    }

    private static char changeBit (char bit){
        char changedBit;
        if (bit=='0') changedBit = '1';
        else changedBit = '0';

        return changedBit;
    }

    private static void writeDecompressedFile(ArrayList<String> decompressedList) throws IOException {
        FileWriter deCompressedFile = new FileWriter("dout.txt");
        BufferedWriter buffer = new BufferedWriter(deCompressedFile);

        for (String decompressedInstruction : decompressedList){
            buffer.write(decompressedInstruction);
            buffer.newLine();
        }

        buffer.close();
        deCompressedFile.close();
    }
}
