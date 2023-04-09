import cv2
import os
import asyncio

async def add_wm(dir,file_name):
    try:
        #start time
        start = cv2.getTickCount()
        img = cv2.imread(f'{dir}/{file_name}',1)
        path = "/Users/gabrielhall/Documents/Work/Livraria/site/BookCreator/utils/watermark.png"
        watermark=cv2.imread(path,1)
        alpha = cv2.imread("utils/alpha_mask.png")
        alpha = alpha.astype(float)/255

        wm_width = int(img.shape[1]*0.35)
        wm_height = wm_width
        wm_dim = (wm_width, wm_height)
        resized_wm = cv2.resize(watermark, wm_dim, interpolation=cv2.INTER_AREA)
        alpha = cv2.resize(alpha, (resized_wm.shape[1], resized_wm.shape[0]), interpolation=cv2.INTER_AREA)
        #replace alpha with black on the watermark
        wm = cv2.multiply(alpha, resized_wm.astype(float))

        h_img, w_img, _ = img.shape
        h_wm, w_wm, _ = resized_wm.shape

        x_offset = int(w_img)-int(w_wm)
        y_offset = int(h_img)-int(h_wm)
        x_end = int(w_img)
        y_end = int(h_img)

        #replace inverted alpha with black on sliced corner from bg
        roi = img[y_offset:y_end,x_offset:x_end]
        background = cv2.multiply(1.0 - alpha, roi.astype(float))
        out = cv2.add(wm, background)
        img[y_offset:y_end,x_offset:x_end] = out

        cv2.imwrite(f'{dir}/{file_name}', img)
        #end time
        end = cv2.getTickCount()
        #calculate time
        time = (end - start)/cv2.getTickFrequency()
        return file_name, time
    except Exception as e:
        print(e)
        return file_name, "[ERROR]"


"""
def get_tasks(dir, file_names):
    tasks = []
    for file in file_names:
        #add new task to queue

        if file.endswith((".jpg",".png",".jpeg")):
            pass
            try:
                print(f'Task [{len(tasks)}]: Adding watermark to {file}')
                tasks.append(add_wm(dir, file))
            except:
                print(f'Task [{len(tasks)}]: Error adding watermark to {file}')
    return tasks

async def main():
    dir = os.getcwd()
    #cd to images
    #for each folder in images open it and call with add_wm(file)
    for (dir, dir_names, file_names) in os.walk(dir+'/manual'):
            #print file name
            tasks = get_tasks(dir, file_names)
            if tasks != None:
                responses = await asyncio.gather(*tasks)
                for filename, time in responses:
                    print(f'Task [{len(tasks)}]: Watermark added to {filename} in {time} seconds')
            
if __name__ == '__main__':
    asyncio.run(main())

"""