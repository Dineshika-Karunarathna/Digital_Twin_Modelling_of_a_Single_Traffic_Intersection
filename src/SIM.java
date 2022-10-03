import java.io.File;
import java.io.FileNotFoundException;
import java.util.*;

public class SIM {
    public static void main(String[] args) throws FileNotFoundException {
        String originalFile = "original.txt";
        ArrayList<String> originalList = readFile(originalFile);
        String compressedFile = "compressed.txt";
        ArrayList<String> compressedList = readFile(compressedFile);

        HashMap<String ,String> dictionary = createDictionary(originalList);

    }

    private static ArrayList<String> readFile(String filePath) throws FileNotFoundException {

        File originalFile = new File(filePath);
        Scanner scanner = new Scanner(originalFile);
        ArrayList<String> originalList = new ArrayList<>();
        while (scanner.hasNextLine()) {
            String entry = scanner.nextLine();
            originalList.add(entry);
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


}
