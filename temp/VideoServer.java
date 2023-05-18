import java.io.*;
import java.net.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Arrays;
import java.util.List;
import java.util.concurrent.*;

public class VideoServer {
    private static final int PORT = 8080;
    private static final int MAX_GAMES = 5;
    private static final int MAX_PLAYERS_PER_GAME = 3;

    private static final ConcurrentHashMap<Integer, Game> games = new ConcurrentHashMap<>();

    public static void main(String[] args) throws IOException {
        for (int i = 0; i < MAX_GAMES; i++) {
            games.put(i, new Game(Game.GameType.MATHEMATIQUES));
        }

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
        private String name;
        private GameType gameType;
        private List<String> mots;
        private List<String> pictionaryWords = Arrays.asList("pomme", "livre", "eclair", "serpent", "la Tour Eiffel", "banane", "avion", "seau", "enveloppe", "carotte", "hache", "reveil", "chat", "enclume", "fleur", "main", "lunettes", "papillon", "triangle", "shorts");
        ConcurrentHashMap<Socket, DataOutputStream> clients = new ConcurrentHashMap<>();
        String valToFind = "1";
        ConcurrentHashMap<Socket, Integer> scores = new ConcurrentHashMap<>();
        public Game(GameType gameType) {
            this.gameType = gameType;
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
        
            return result + ";" + num1 + operator + num2;
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
            //Send to all clients the new value to find with a blank image and a score of 0
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
                        gamesString += "Game " + (i+1) + " : " + games.get(i).clients.size() + "/" + MAX_PLAYERS_PER_GAME + " "+games.get(i).getType() +  ";";
                    }
                    outputWriter.println(gamesString);
                    clientSocket.close();
                }
                else{
                    username = receivedMessage.split(";")[0];
                    idServer = Integer.parseInt(receivedMessage.split(";")[1]);
                }

                int servIndexUser = idServer;
                Game game = games.get(idServer);


                if (game.clients.size() < ) {
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
                        if(game.scores.get(clientSocket) == 5){
                            for (Socket socket : game.clients.keySet()) {
                                socket.close();
                            }
                            //remove all players from the game
                            game.clients.clear();
                            game.scores.clear();
                            
                        }
                    }
                }
            } catch (IOException e) {
                //Print that user left
                System.out.println("Client " + clientSocket.getRemoteSocketAddress() + " s'est déconnecté");
                //e.printStackTrace();
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

