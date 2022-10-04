import java.io.File;
import java.io.FileNotFoundException;
import java.util.*;

public class SIM {
    public static void main(String[] args) throws FileNotFoundException {
        String originalFile = "original2.txt";
        ArrayList<String> originalList = readFile(originalFile);
        //String compressedFile = "compressed.txt";
        //ArrayList<String> compressedList = readFile(compressedFile);

        compression(originalList);
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
        return selectEntries(entryFrequency, frequencies);
    }

    private static HashMap<String, String> selectEntries(HashMap<String,Integer> entryFrequency, ArrayList<Integer> frequencies){
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

    private static void compression(ArrayList<String> originalList){
        ArrayList<String> compressedInstructions = new ArrayList<>();

        HashMap<String ,String> dictionary = createDictionary(originalList);
        System.out.println(dictionary);

        checkConsecutiveRepetitions (originalList);

        for (String entry: originalList){
            String instructionToCompress = entry.substring(0,32);
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

        String beneficialCompression = compressionFormats.get(0);
        for (String format: compressionFormats) {
            if (format.length()>2 && (format.length() < beneficialCompression.length())) {
                beneficialCompression = format;
            }
        }
        return beneficialCompression;
    }

    private static String rleCompression(int rleCount){
        String countToBinary = Integer.toBinaryString(rleCount-1);

        return "000"+ countToBinary;
    }

    private static String bitMaskBasedCompression(String instruction, HashMap<String, String> dictionary){
        StringBuilder compressedInstruction = new StringBuilder("001");

        return compressedInstruction.toString();
    }

    private static String oneBitMismatchCompression(String instruction, HashMap<String, String> dictionary){
        StringBuilder compressedInstruction = new StringBuilder("010");

        return compressedInstruction.toString();
    }

    private static String twoBitConsecutiveMismatchCompression(String instruction, HashMap<String, String> dictionary){
        StringBuilder compressedInstruction = new StringBuilder("011");

        return compressedInstruction.toString();
    }

    private static String twoBitMismatchCompression(String instruction, HashMap<String, String> dictionary){
        StringBuilder compressedInstruction = new StringBuilder("100");

        return compressedInstruction.toString();
    }

    private static String directMatchingCompression(String instruction, HashMap<String, String> dictionary){
        StringBuilder compressedInstruction = new StringBuilder("101");
        for(Map.Entry<String, String> entry : dictionary.entrySet()){
            if (instruction.equals(entry.getKey())){
                compressedInstruction.append(entry.getValue());
            }
        }
        return compressedInstruction.toString();
    }

    private static String originalBinariesCompression(String instruction){

        return "110" + instruction;
    }
}
