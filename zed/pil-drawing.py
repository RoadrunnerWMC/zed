IMGW, IMGH = 500, 500
import PIL.Image, PIL.ImageDraw, PIL.ImageFont
image = PIL.Image.new('RGBA', (IMGW, IMGH), (0,0,0,0))

stuff.append((True, npcType, xPos, yPos))

# draw = PIL.ImageDraw.Draw(image)
# font = PIL.ImageFont.truetype('/usr/share/fonts/truetype/noto/NotoMono-Regular.ttf', 16)

# minX = minY = 0xFFFF
# maxX = maxY = 0
# for isNpc, objType, xPos, yPos in stuff:
#     if xPos < minX: minX = xPos
#     if yPos < minY: minY = yPos
#     if xPos > maxX: maxX = xPos
#     if yPos > maxY: maxY = yPos
# maxX += 1; maxY += 1

# if minX < 0xFFFF and minY < 0xFFFF:
#     for isNpc, objType, xPos, yPos in stuff:
#         x = IMGW * (xPos - minX) / (maxX - minX)
#         y = IMGH * (yPos - minY) / (maxY - minY)
#         color = (0,0,0,255) if isNpc else (255,0,0,255)
#         draw.text((x, y), objType, color, font=font)

return image


courseImg = parseZmb(zmbFile)
        courseImg.save(f'courses/{courseFilename}.png')



# Record ZAB sizes:
# dngn_main
# d_main