import random
import string
from realmain import *
actualScore = 0
fontMOT = pygame.font.Font('freesansbold.ttf', 60)
def setGameType(gameType):
    if(gameType == "Pictionary"):
        return modelDraw
    elif(gameType == "Mots"):
        return modelLetters
    elif(gameType == "Mathématiques"):
        return model

def predictImage(typeGame):
    if(typeGame == "Pictionary"):
        valFinded = predict(preprocess_image("Imgs/canvas.jpg",typeGame), modelDraw,typeGame)
    elif(typeGame == "Mots"):
        valFinded = predict(preprocess_image("Imgs/canvas.jpg",typeGame), modelLetters,typeGame)
        print(valFinded)
    elif(typeGame == "Mathématiques"):
        valFinded = predict(preprocess_image("Imgs/canvas.jpg",typeGame), model,typeGame)
        print(valFinded)
    window.blit(buttonValFinded, (750, 150))
    textVal = font.render(str(valFinded), True, (255, 255, 255))
    window.blit(textVal, (825, 165))
    return valFinded

def generateOtherValToFind(typeGame):
    if(typeGame == "Pictionary"):
        #Pick a random word from objet_name array
        return random.choice(objet_names)
    elif (typeGame == "Mots"):
        #Generate random letter
        with open("Mots.txt", "r") as file:
            words = file.readlines()
        word_to_find = random.choice(words).strip()
        print("Mot à trouver : " + word_to_find)
        return word_to_find
    elif (typeGame == "Mathématiques"):
        result = random.randint(0, 9)

        operator = random.choice(["+", "-", "*", "//"])

        if operator == "+":
            num1 = random.randint(0, result)
            num2 = result - num1
        elif operator == "-":
            num1 = random.randint(result, 1000)
            num2 = num1 - result
        elif operator == "*":
            num1 = random.choice([i for i in range(1, 10) if result % i == 0])
            num2 = result // num1
        else: # operator == "//"
            num1 = random.randint(1, 9)
            num2 = num1 * result
            while num2 == 0: # Check for division by 0
                num1 = random.randint(1, 9)
                num2 = num1 * result
            return str(result) + ";" + str(num2) + operator + str(num1)

        math_problem = f"{num1} {operator} {num2}"
        print("Calcul à résoudre : " + math_problem)
        return str(result)+ ";" + str(num1) + operator + str(num2)

        #return predict_draw(preprocess_image("Imgs/canvas.jpg"), modelDraw)

def display_current_word(word, letters_found):
    displayed_word = ""
    for letter in word:
        if letter in letters_found:
            displayed_word += letter
        else:
            displayed_word += " "
    return displayed_word
        

def mainSolo(isonline,gameType):
    valToFind = generateOtherValToFind(gameType)
    letters_found = set()
    current_letter_index = 0
    
    init(gameType)
    if(gameType == "Mathématiques"):
        setNewValue(gameType,valToFind.split(";")[1])
        valToFind = valToFind.split(";")[0]
    else:
        setNewValue(gameType,valToFind)
    score = 0   
    currentModel = setGameType(gameType)
    gomme = True
    tmpcordX = -1
    tmpcordY = -1
    #servIndexUser = servIndex
    username = ""

    print("Valeur a trouver : " + str(valToFind))
    if(isonline == "Solo"):
        start_time = time.time()
        clock = pygame.time.Clock()

    while True:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
                        print("photo")
                        try:
                            valFinded = predictImage(gameType)
                            print("Valeur à trouver " + str(valToFind) + "Valeur trouvée " + str(valFinded))
                            if gameType == "Mots":
                                if valToFind[current_letter_index] == valFinded:
                                    print("Lettre trouvée dans l'ordre !")
                                    lettertodraw = fontMOT.render(str(valFinded), True, (0, 255, 0))
                                    window.blit(lettertodraw, (800+(current_letter_index*60), 300))
                                    letters_found.add(valFinded)
                                    current_letter_index += 1
                                    if current_letter_index == len(valToFind):
                                        print("Toutes les lettres du mot ont été trouvées dans l'ordre !")
                                        current_letter_index = 0
                                        letters_found.clear()
                                        score += 1
                                        init(gameType)
                                        valToFind = generateOtherValToFind(gameType)
                                        setNewValue(gameType,valToFind)
                            if str(valToFind) == str(valFinded):
                                print("trouvé")
                                score += 1
                                if(gameType == "Mathématiques"):
                                    valToFindTMP = generateOtherValToFind(gameType)
                                    valToFind = valToFindTMP.split(";")[0]
                                    calculus = valToFindTMP.split(";")[1]
                                    setNewValue(gameType,calculus)
                                else:
                                    valToFind = generateOtherValToFind(gameType)
                                    setNewValue(gameType,valToFind)
                                canvasToSave[:] = 255, 255, 255
                                canvas[:] = 0, 0, 0
                                
                        except Exception as e:
                            print("error")
                            print(e)

        pygame.display.update()
        if keys[pygame.K_w]:
            canvasToSave[:] = 255, 255, 255
            canvas[:] = 0, 0, 0

        if keys[pygame.K_x]:
             gomme = not gomme
        
        #print(valToFind)
        pygame.display.update()

        success, img = cap.read()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)

        cv2.rectangle(img, (100, 50), (450, 400), (0, 255, 0), 2)
        if results.multi_hand_landmarks and len(results.multi_hand_landmarks) == 2 and has2Hands == False:
            has2Hands = True
            if has2Hands:
                print("2 mains détectées")

        if results.multi_hand_landmarks and len(results.multi_hand_landmarks) == 1:  # Now detect only one hand
            has2Hands = False
            for handLms in results.multi_hand_landmarks:
                for id, lm in enumerate(handLms.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    if id == 8:
                        # print("Coords de 8", cx, cy)
                        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
                        tmpx8 = cx
                        tmpy8 = cy
                        if tmpx8 != 0 and tmpy8 != 0:
                            tmpx8 = 640 - tmpx8

                            drawLine(tmpx8, tmpy8, tmpcordX, tmpcordY, gomme)
                            tmpcordX = tmpx8
                            tmpcordY = tmpy8

                mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

        else:
            tmpcordX = -1
            tmpcordY = -1
        img = cv2.flip(img, 1)
        # cv2.imshow("Image", img)
        cv2.addWeighted(canvas, 1, img, 1, 1, img)
        # cv2.imshow("Image", img)
        cv2.waitKey(1)

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        if(isonline == "Solo"):
            elapsed_time = time.time() - start_time
            remaining_time = max(0, 25 - elapsed_time)
            minutes = int(remaining_time / 60)
            seconds = int(remaining_time % 60)
            timer_text = f"{minutes:02d}:{seconds:02d}"
            timer_surface = font.render(timer_text, True, (255, 255, 255))
            window.blit(butTimer, (1280 - 200, 720 - 100))
            window.blit(timer_surface, (1280 - 150, 720 - 75))
            if remaining_time <= 0:
                win(str(score))
                break
            clock.tick(60)

        frame = img_rgb
        frame = np.rot90(frame)

        frame = pygame.surfarray.make_surface(frame)
        frameCanvas = pygame.surfarray.make_surface(img_rgb)

        frameCanvas = pygame.transform.rotate(frameCanvas, 90)

        frameCanvas = pygame.transform.flip(frameCanvas, False, True)
        window.blit(frameCanvas, (0, 0))

        text = font.render("Score : " + str(score), True, (255, 255, 255))
        window.blit(text, (500, 0))

        # Save canvas to image
        byteFrame = pygame.image.tostring(frameCanvas, 'RGBA')





