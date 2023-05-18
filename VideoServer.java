import java.io.*;
import java.net.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Arrays;
import java.util.List;
import java.util.Random;
import java.util.concurrent.*;
import java.util.ArrayList;
public class VideoServer {
    private static final int PORT = 8080;
    private static final int MAX_GAMES = 8;
    private static int NB_ACTUAL_GAMES = 0;
    private static final int SCORE_TO_WIN = 3;

    private static final ConcurrentHashMap<Integer, Game> games = new ConcurrentHashMap<>();

    public static void deleteGamesWithIsGameFinished() {
        List<Integer> keysToRemove = new ArrayList<>();
        
        for (Integer key : games.keySet()) {
            if (games.get(key).isGameFinished == 1) {
                keysToRemove.add(key);
                System.out.println("Partie supprimée " + key);
            }
        }
        
        for (Integer key : keysToRemove) {
            games.remove(key);
            NB_ACTUAL_GAMES--;
        }
        
        // Décaler les indices pour qu'il n'y ait pas de trou
        ConcurrentHashMap<Integer, Game> updatedGames = new ConcurrentHashMap<>();
        int newIndex = 0;
        
        for (Integer key : games.keySet()) {
            updatedGames.put(newIndex, games.get(key));
            newIndex++;
        }
        
        games.clear();
        games.putAll(updatedGames);
    }
    
    public static void main(String[] args) throws IOException {
        games.put(0, new Game(Game.GameType.PICTIONARY,"Default",2));
        NB_ACTUAL_GAMES++;   //On fait une game défaut
        try (ServerSocket serverSocket = new ServerSocket(PORT)) {
            System.out.println("Serveur en attente de connexions...");
            while (true) {
                Socket clientSocket = serverSocket.accept();
                System.out.println("Client connecté: " + clientSocket.getRemoteSocketAddress());
                new Thread(new ClientHandler(clientSocket)).start();
            }
        }
    }

    static class Game {
        public enum GameType {
            MATHEMATIQUES, MOTS, PICTIONARY
        }
        private int isGameFinished = 0;
        private String name;
        private GameType gameType;
        private final int maxplayergame;
        private List<String> mots;
        private List<String> pictionaryWords = Arrays.asList("pomme", "livre", "eclair", "serpent", "la Tour Eiffel", "banane", "avion", "seau", "enveloppe", "carotte", "hache", "reveil", "chat", "enclume", "fleur", "main", "lunettes", "papillon", "triangle", "shorts");
        ConcurrentHashMap<Socket, DataOutputStream> clients = new ConcurrentHashMap<>();
        String valToFind = "1";
        ConcurrentHashMap<Socket, Integer> scores = new ConcurrentHashMap<>();
        public Game(GameType gameType, String name, int maxplayergame) {
            this.gameType = gameType;
            this.name = name;
            this.maxplayergame = maxplayergame;
            if (gameType == GameType.MOTS) {
                try {
                    mots = Files.readAllLines(Paths.get("Mots.txt"));
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
            updateValToFind();
        }
        public String getType() {
            return gameType.toString();
        }
        public String getName() {
            return name;
        }

        public static String generateMathProblem() {
            Random random = new Random();
            int result = random.nextInt(10);
            String operator = "";
            int num1 = 0;
            int num2 = 0;

            switch (random.nextInt(4)) {
                case 0:
                    operator = "+";
                    num1 = random.nextInt(result + 1);
                    num2 = result - num1;
                    break;
                case 1:
                    operator = "-";
                    num1 = random.nextInt(1000 - result) + result;
                    num2 = num1 - result;
                    break;
                case 2:
                    operator = "*";
                    int[] factors = {1, 2, 3, 4, 5, 6, 7, 8, 9};
                    for (int i = factors.length - 1; i >= 0; i--) {
                        if (result % factors[i] == 0) {
                            num1 = factors[i];
                            num2 = result / num1;
                            break;
                        }
                    }
                    break;
                case 3:
                    operator = "//";
                    while (num2 == 0) {
                        num1 = random.nextInt(9) + 1;
                        num2 = num1 * result;
                    }
                    break;
            }

            String mathProblem = String.format("%d %s %d", num1, operator, num2);
            System.out.println("Calcul à résoudre : " + mathProblem);

            return result + ";" + num2 + operator + num1;
        }
        public void updateValToFind() {
            switch (gameType) {
                case MATHEMATIQUES:
                    valToFind = generateMathProblem();
                    break;
                case MOTS:
                    valToFind = mots.get((int) (Math.random() * mots.size()));
                    break;
                case PICTIONARY:
                    valToFind = pictionaryWords.get((int) (Math.random() * pictionaryWords.size()));
                    break;
            }
            for (Socket client : clients.keySet()) {
                if (scores.get(client) == SCORE_TO_WIN) {
                    System.out.println("Partie finie");
                    isGameFinished = 1;
                }
            }
            if (isGameFinished == 1) {
                if(this.clients.size()>0){
                    try {
                        Thread.sleep(100);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                    for (Socket client2 : clients.keySet()) {
                        try {
                            client2.close();
                        } catch (IOException e) {
                            e.printStackTrace();
                        }
                    }
                    System.out.println("Partie finie");
                    deleteGamesWithIsGameFinished();
                    System.out.println("deleted");
                }
            }
        }
    }

    static class ClientHandler implements Runnable {
        private final Socket clientSocket;
        private String username;
        private int idServer;

        public ClientHandler(Socket clientSocket) {
            this.clientSocket = clientSocket;
        }

        @Override
        public void run() {
            try {
                DataInputStream inputStream = new DataInputStream(clientSocket.getInputStream());
                DataOutputStream outputStream = new DataOutputStream(clientSocket.getOutputStream());
                BufferedReader inputReader = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
                PrintWriter outputWriter = new PrintWriter(clientSocket.getOutputStream(), true);

                String receivedMessage = inputReader.readLine();
                System.out.println("Received message: " + receivedMessage);

                // Si le message est "defaultUser", renvoyez "salut" et terminez le thread
                if ("hello".equalsIgnoreCase(receivedMessage)) {
                    //Print all the games and their number of players
                    String gamesString = "";
                    for (int i = 0; i < MAX_GAMES; i++) {
                        if(games.get(i)!=null){
                            gamesString += games.get(i).name + " : " + games.get(i).clients.size() + "/" + games.get(i).maxplayergame + " "+games.get(i).getType() +  ";";
                        }
                    }
                    outputWriter.println(gamesString);
                    clientSocket.close();
                }
                else if ("createserver".equalsIgnoreCase(receivedMessage.split(";")[0])){
                    //msg with have the form "createserver;gameType;gameName;slots"
                    String gameType = receivedMessage.split(";")[1].toUpperCase();
                    String gameName = receivedMessage.split(";")[2];
                    int slots = Integer.parseInt(receivedMessage.split(";")[3]);
                    Game game = new Game(Game.GameType.valueOf(gameType), gameName, slots);
                    games.put(NB_ACTUAL_GAMES, game);
                    NB_ACTUAL_GAMES++;
                    String gamesString = "";
                    for (int i = 0; i < NB_ACTUAL_GAMES; i++) {
                        gamesString += games.get(i).name + " : " + games.get(i).clients.size() + "/" + games.get(i).maxplayergame + " "+games.get(i).getType() +  ";";
                    }
                    outputWriter.println(gamesString);
                    clientSocket.close();
                }
                else{
                    username = receivedMessage.split(";")[0];
                    idServer = Integer.parseInt(receivedMessage.split(";")[1]);

                    int servIndexUser = idServer;
                    Game game = games.get(idServer);


                    if (game.clients.size() < game.maxplayergame) {
                        game.clients.put(clientSocket, outputStream);
                        game.scores.put(clientSocket, 0);
                        System.out.println("Client " + clientSocket.getRemoteSocketAddress() + " ajouté à la partie " + servIndexUser);

                        if (game.clients.size() == 1) {
                            game.updateValToFind();
                        }
                        for (DataOutputStream out : game.clients.values()) {
                            out.writeInt(450);
                            System.out.print("Valeur à trouver score update " + game.valToFind);
                            String value = String.valueOf(game.valToFind);
                            out.writeInt(value.length());
                            out.write(value.getBytes(StandardCharsets.UTF_8));
                        }
                    } else {
                        //Send to the client that the game is full
                        outputStream.writeInt(400);
                        throw new IOException("Partie pleine");
                    }

                    while (true) {
                        int score = inputStream.readInt();
                        int length = inputStream.readInt();
                        if (length > 0) {
                            byte[] image = new byte[length];
                            inputStream.readFully(image, 0, length);
                            //System.out.println("Image reçue");
                            if (game.scores.get(clientSocket) != score) {
                                game.scores.put(clientSocket, score);
                                game.updateValToFind();
                                for (DataOutputStream out : game.clients.values()) {
                                    out.writeInt(500);
                                    System.out.print("Valeur à trouver score update " + game.valToFind);
                                    String value = String.valueOf(game.valToFind);
                                    out.writeInt(value.length());
                                    out.write(value.getBytes(StandardCharsets.UTF_8));
                                }

                            }

                            game.clients.entrySet().stream()
                                    .filter(entry -> entry.getKey() != clientSocket)
                                    .forEach(entry -> {
                                        try {
                                            entry.getValue().writeInt(2);
                                            entry.getValue().writeInt(score);
                                            entry.getValue().writeInt(length);
                                            entry.getValue().write(image);
                                            String userToSend = username + "\0";
                                            byte[] usernameBytes = userToSend.getBytes(StandardCharsets.UTF_8);
                                            entry.getValue().writeInt(usernameBytes.length);
                                            entry.getValue().write(usernameBytes);
                                            //System.out.println("Envoie image venant de " + username + " à " + entry.getKey().getRemoteSocketAddress());
                                        } catch (IOException e) {
                                            System.out.println("ERREUR LORS DE L'ENVOI DU MESSAGE");
                                            e.printStackTrace();
                                        }
                                    });
                        }
                    }
                }
            } catch (IOException e) {
                System.out.println("Client " + clientSocket.getRemoteSocketAddress() + " s'est déconnecté");
            } finally {
                Game game = games.values().stream().filter(g -> g.clients.containsKey(clientSocket)).findFirst().orElse(null);

                if (game != null) {
                    game.clients.remove(clientSocket);
                    game.scores.remove(clientSocket);

                }

                try {
                    clientSocket.close();
                } catch (IOException e) {
                    System.out.println("ERREUR LORS FERMETURE SOCKET");
                    e.printStackTrace();
                }
            }
        }
    }
}

