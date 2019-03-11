x = 0
y = 0
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)

import pygame
import csv
from operator import itemgetter

# GLOBALS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BGROUND = (38, 38, 38)
THSCOL = (222, 0, 55)
LBWCOL = (0, 222, 69)

# Files to be analyzed
infiles = ["C:/Users/ccros/PycharmProjects/untitled1/keywordsTHS.csv", "C:/Users/ccros/PycharmProjects/untitled1/sentencesTHS.csv",
           "C:/Users/ccros/PycharmProjects/untitled1/keywordsLBW.csv", "C:/Users/ccros/PycharmProjects/untitled1/sentencesLBW.csv"]


# Setup
pygame.init()
size = (1600, 900)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Text Analysis")

# Loop until the user clicks the close button.
done = False

# Used to manage frame rate
clock = pygame.time.Clock()



# -------------------------- Document Class --------------------------

def load_files(filename):
    with open(filename) as csvfile:
        readCSV = csv.reader(csvfile)
        myList = list(readCSV)
    return myList

class Doc:
    def __init__(self, keywords, sentences):
        self.keywords = keywords
        self.sentences = sentences
        self.avg_word = 0
        self.avg_sent = 0
        self.total_word = 0
        self.total_sent = 0
        self.tick = 0
        self.spot = 0
        self.stop = 0
        self.last_tick = 0
        self.i = 0
        self.x = [["firstword", 0]]

    def uptick(self):
        self.tick += 1

    def get_total_word(self, tick):
        self.total_word += (len(self.keywords[tick][0]))
        return self.total_word

    def get_avg_word(self):
        curr = self.get_total_word(self.tick)
        avg = curr / self.tick
        return avg

    def get_total_sent(self):
        k = self.spot
        if (k >= len(self.sentences) - 1):
            total = self.total_sent
            return total
        temp = 0
        while (self.sentences[k][0] != "."):
            temp += 1
            k += 1

        self.spot = k + 1
        self.total_sent += temp
        total = self.total_sent
        return total

    def get_avg_sent(self):
        curr = self.get_total_sent()
        if (curr == self.stop):
            self.last_tick = self.tick - self.i
            self.i += 1
            avg = curr / self.last_tick
        else:
            avg = curr / self.tick
        self.stop = curr
        return avg

    def top_words(self):
        indict = False
        word = self.keywords[self.tick][0]
        for i in range (0, len(self.x)):
            if (self.x[i][0] == word):
                self.x[i][1] += 1
                indict = True;
        if (indict != True):
            self.x.append([word, 0])

        self.x = sorted(self.x, key=itemgetter(1))

        return (self.x[-5:])



# -------------------------- End Document Class --------------------------


THS = Doc(load_files(infiles[0]), load_files(infiles[1]))
LBW = Doc(load_files(infiles[2]), load_files(infiles[3]))


# -------------------------- Main Program Loop --------------------------

while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True


    # Step through analysis
    THS.uptick()
    LBW.uptick()
    topwordsTHS = (THS.top_words())
    topwordsLBW = (LBW.top_words())

    wTHS = round(THS.get_avg_word(), 2)
    sTHS = round(THS.get_avg_sent(), 2)

    wLBW = round(LBW.get_avg_word(), 2)
    sLBW = round(LBW.get_avg_sent(), 2)


    # Screen-clearing
    screen.fill(BGROUND)

    # Drawing
    pygame.draw.rect(screen, THSCOL, [0, 225, wTHS * 50, 50])
    pygame.draw.rect(screen, THSCOL, [0, 300, sTHS * 30, 50])

    pygame.draw.rect(screen, LBWCOL, [0, 675, wLBW * 50, 50])
    pygame.draw.rect(screen, LBWCOL, [0, 750, sLBW * 30, 50])

    font = pygame.font.SysFont('Calibri', 20, True, False)
    text = font.render("Average Word Length: " + str(wTHS), True, WHITE)
    screen.blit(text, [10, 242])
    font = pygame.font.SysFont('Calibri', 20, True, False)
    text = font.render("Average Sentence Length: " + str(sTHS), True, WHITE)
    screen.blit(text, [10, 317])


    font = pygame.font.SysFont('Calibri', 20, True, False)
    text = font.render("Average Word Length: " + str(wLBW), True, WHITE)
    screen.blit(text, [10, 692])
    font = pygame.font.SysFont('Calibri', 20, True, False)
    text = font.render("Average Sentence Length: " + str(sLBW), True, WHITE)
    screen.blit(text, [10, 767])

    for i in range (0, len(topwordsTHS)):
        mySize = 20 + 3 * i
        font = pygame.font.SysFont('Calibri', mySize, True, False)
        text = font.render(topwordsTHS[i][0], True, WHITE)
        screen.blit(text, [1300 - 130 * i, 225 + (len(topwordsTHS) - i)])

        text = font.render(topwordsLBW[i][0], True, WHITE)
        screen.blit(text, [1300 - 130 * i, 675 + (len(topwordsLBW) - i)])

    font = pygame.font.SysFont('Calibri', 45, True, False)
    text = font.render("This House of Sky", True, WHITE)
    screen.blit(text, [600, 60])
    pygame.draw.rect(screen, WHITE, [600, 108, 320, 3])

    font = pygame.font.SysFont('Calibri', 45, True, False)
    text = font.render("Last Bus to Wisdom", True, WHITE)
    screen.blit(text, [580, 500])
    pygame.draw.rect(screen, WHITE, [580, 548, 370, 3])


    # Flip to display
    pygame.display.flip()

    # Set frame rate
    clock.tick(60)


# Close the window and quit.
pygame.quit()