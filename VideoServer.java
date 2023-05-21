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
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

public class VideoServer {
    private static final int PORT = 8080; // Port sur lequel le serveur écoute
    private static final int MAX_GAMES = 8; // Nombre maximum de parties de jeu autorisées
    private static int NB_ACTUAL_GAMES = 0; // Nombre de parties de jeu en cours actuellement
    private static final int SCORE_TO_WIN = 10; // Score requis pour gagner la partie

    // Stockage des parties de jeu en cours
    private static final ConcurrentHashMap<Integer, Game> games = new ConcurrentHashMap<>();
    private static final Lock gamesLock = new ReentrantLock();
    private static ArrayList<Integer> disconnectedIndices = new ArrayList<>(); // Indices des clients déconnectés

    // Supprime les parties de jeu terminées
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
        // Initialisation des parties de jeu
        for (int i = 0; i < 1; i++) {
            games.put(i, new Game(Game.GameType.PICTIONARY, "Default", 4));
            NB_ACTUAL_GAMES++;   // On fait une game défaut
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
        // Types de jeu disponibles
        public enum GameType {
            MATHEMATIQUES, MOTS, PICTIONARY
        }

        private int isGameFinished = 0; // Indique si la partie de jeu est terminée (1 = terminée, 0 = en cours)
        private String name; // Nom de la partie de jeu
        private GameType gameType; // Type de jeu
        private final int maxplayergame; // Nombre maximum de joueurs dans la partie de jeu
        private List<String> mots; // Liste de mots pour le jeu "Mots"
        private List<String> pictionaryWords = Arrays.asList(
                "POMME", "ECLAIR", "AVION", "SEAU", "CHAPEAU", "ENVELOPPE", "CAROTTE", "HACHE",
                "CUILLERE", "CHAT", "PORTE", "ENCLUME", "FLEUR", "BUS", "MAIN", "POISSON", "LUNETTES", "PAPILLON",
                "NUAGE", "TRIANGLE", "SHORTS"
        ); // Liste de mots pour le jeu "Pictionary"
        ConcurrentHashMap<Socket, DataOutputStream> clients = new ConcurrentHashMap<>(); // Clients connectés à la partie de jeu
        ConcurrentHashMap<Socket, Integer> clientIndices = new ConcurrentHashMap<>(); // Indices des clients dans la partie de jeu
        String valToFind = "1"; // Valeur à trouver dans la partie de jeu
        ConcurrentHashMap<Socket, Integer> scores = new ConcurrentHashMap<>(); // Scores des clients dans la partie de jeu
        private final Lock gameLock = new ReentrantLock(); // Verrou pour la synchronisation

        public Game(GameType gameType, String name, int maxplayergame) {
            this.gameType = gameType;
            this.name = name;
            this.maxplayergame = maxplayergame;
            if (gameType == GameType.MOTS) {
                try {
                    mots = Files.readAllLines(Paths.get("Mots.txt")); // Chargement des mots depuis un fichier
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

        // Génère un problème mathématique aléatoire
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
                    while (num1 == 0) {
                        num2 = random.nextInt(9) + 1;
                        num1 = num2 * result;
                    }
                    break;
            }

            String mathProblem = String.format("%d %s %d", num1, operator, num2);
            System.out.println("Calcul à résoudre : " + mathProblem);

            return result + ";" + num1 + operator + num2;
        }

        // Met à jour la valeur à trouver en fonction du type de jeu
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

            // Vérifie si un client a atteint le score requis pour gagner la partie
            for (Socket client : clients.keySet()) {
                if (scores.get(client) == SCORE_TO_WIN) {
                    System.out.println("Partie finie");
                    isGameFinished = 1;
                }
            }

            // Si la partie est terminée, ferme les connexions des clients et supprime la partie de jeu
            if (isGameFinished == 1) {
                if (this.clients.size() > 0) {
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
        private int clientIndex; // Stocker l'indice pour le client

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

                // Si le message est "askserverforplayers", renvoie la liste des jeux et leur nombre de joueurs
                if ("askserverforplayers".equalsIgnoreCase(receivedMessage)) {
                    String gamesString = "";
                    for (int i = 0; i < MAX_GAMES; i++) {
                        if (games.get(i) != null) {
                            gamesString += games.get(i).name + " : " + games.get(i).clients.size() + "/" + games.get(i).maxplayergame + " " + games.get(i).getType() + ";";
                        }
                    }
                    outputWriter.println(gamesString);
                    clientSocket.close();
                } else if ("createserver".equalsIgnoreCase(receivedMessage.split(";")[0])) {
                    // Le message a la forme "createserver;gameType;gameName;slots"
                    String gameType = receivedMessage.split(";")[1].toUpperCase();
                    String gameName = receivedMessage.split(";")[2];
                    int slots = Integer.parseInt(receivedMessage.split(";")[3]);

                    gamesLock.lock();
                    try {
                        Game game = new Game(Game.GameType.valueOf(gameType), gameName, slots);
                        games.put(NB_ACTUAL_GAMES, game);
                        NB_ACTUAL_GAMES++;
                    } finally {
                        gamesLock.unlock();
                    }

                    String gamesString = "";
                    gamesLock.lock();
                    try {
                        for (int i = 0; i < NB_ACTUAL_GAMES; i++) {
                            gamesString += games.get(i).name + " : " + games.get(i).clients.size() + "/" + games.get(i).maxplayergame + " " + games.get(i).getType() + ";";
                        }
                    } finally {
                        gamesLock.unlock();
                    }

                    outputWriter.println(gamesString);
                    clientSocket.close();
                } else {
                    username = receivedMessage.split(";")[0];
                    idServer = Integer.parseInt(receivedMessage.split(";")[1]);

                    gamesLock.lock();
                    try {
                        Game game = games.get(idServer);

                        if (game != null && game.clients.size() < game.maxplayergame) {
                            if (!disconnectedIndices.isEmpty()) {
                                clientIndex = disconnectedIndices.remove(0);
                                System.out.println("Indice récupéré : " + clientIndex);
                            } else {
                                clientIndex = game.clients.size() + 1; // Assigner l'indice pour le client
                            }

                            game.clients.put(clientSocket, outputStream);
                            game.scores.put(clientSocket, 0);
                            game.clientIndices.put(clientSocket, clientIndex);
                            System.out.println("Client " + clientSocket.getRemoteSocketAddress() + " ajouté à la partie " + idServer + " avec l'index " + clientIndex);

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
                            // Envoyer au client que la partie est pleine
                            outputStream.writeInt(400);
                            throw new IOException("Partie pleine");
                        }
                    } finally {
                        gamesLock.unlock();
                    }

                    while (true) {
                        int score = inputStream.readInt();
                        int length = inputStream.readInt();
                        if (length > 0) {
                            byte[] image = new byte[length];
                            inputStream.readFully(image, 0, length);

                            gamesLock.lock();
                            try {
                                Game game = games.values().stream().filter(g -> g.clients.containsKey(clientSocket)).findFirst().orElse(null);

                                if (game != null) {
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
                                                    entry.getValue().writeInt(clientIndex);
                                                    entry.getValue().writeInt(length);
                                                    entry.getValue().write(image);
                                                    String userToSend = username + "\0";
                                                    byte[] usernameBytes = userToSend.getBytes(StandardCharsets.UTF_8);
                                                    entry.getValue().writeInt(usernameBytes.length);
                                                    entry.getValue().write(usernameBytes);
                                                } catch (IOException e) {
                                                    System.out.println("ERREUR LORS DE L'ENVOI DU MESSAGE");
                                                    e.printStackTrace();
                                                }
                                            });
                                }
                            } finally {
                                gamesLock.unlock();
                            }
                        }
                    }
                }
            } catch (IOException e) {
                System.out.println("Client " + clientSocket.getRemoteSocketAddress() + " s'est déconnecté");
            } finally {
                gamesLock.lock();
                try {
                    Game game = games.values().stream().filter(g -> g.clients.containsKey(clientSocket)).findFirst().orElse(null);

                    if (game != null) {
                        game.clients.remove(clientSocket);
                        game.scores.remove(clientSocket);
                        disconnectedIndices.add(game.clientIndices.get(clientSocket));
                        System.out.println("Indice " + game.clientIndices.get(clientSocket) + " removed");
                        game.clientIndices.remove(clientSocket);
                    }
                } finally {
                    gamesLock.unlock();
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
