import java.io.*;
import java.util.*;

public class SIM {
    public static void main(String[] args) throws IOException {
        String originalFile = "original.txt";

        compression(originalFile);
    }

    public static void compression(String originalFile) throws IOException {
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

        System.out.println(compressedInstructions);
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

    public static void writeCompressedFile(List<String> compressedInstructionList, HashMap<String, String> dictionary) throws IOException {
        StringBuilder compressedText = new StringBuilder();

        for (String compressedInstruction : compressedInstructionList){
            compressedText.append(compressedInstruction);
        }
        int addOnes = compressedText.length()%32;
        if (addOnes>0){
            compressedText.append("1".repeat(32-addOnes));
        }

        FileWriter compressedFile = new FileWriter("compressed.txt");
        BufferedWriter buffer = new BufferedWriter(compressedFile);

        for (int i = 0; i < compressedText.length(); i+=32){
            buffer.write(compressedText.substring(i,i+32));
            buffer.newLine();
        }

        buffer.write("xxxxxxxx");
        buffer.newLine();

        for(String dictionaryEntry:  dictionary.keySet()){
            buffer.write(dictionaryEntry);
            buffer.newLine();
        }

        buffer.close();
        compressedFile.close();

    }

}
