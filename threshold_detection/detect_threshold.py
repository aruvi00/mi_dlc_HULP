
# External Dependencies
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import skimage.segmentation as seg 

## --- MODIFICA LA IMAGEN QUE QUIERES USAR
img_name = "raton1.png"
## ---------------------------------------

# Cargamos la Imagen
rows = 1; colums = 3
img_raw = Image.open(f'C:\\Users\\ainho\\OneDrive\\Escritorio\\UPM4\\TFG\\mi_codigo\\threshold_detection\\test_images\\raton1.png')
img_raw = np.array(img_raw)
plt.title("Imagen Importada")
print("Values Range:", np.max(img_raw), np.min(img_raw))
print("Shape de la Imagen importada:", img_raw.shape)
plt.imshow(img_raw); plt.show()

# Seleccionamos la zona de interes
x_start = 500; x_end = 1000
y_start = 300; y_end = 500
img = img_raw[y_start:y_end,x_start:x_end,0]
print("Shape de imagen recortada:", img.shape)
plt.subplot(rows,colums,1)
plt.title("Zona en la que calcular la recta")
plt.imshow(img)

# Segmentamos el palo
mask = seg.chan_vese(
    img, mu=100, lambda1=100, lambda2=100, tol=1e-3,
    max_num_iter=40, dt=1, init_level_set="checkerboard",
    extended_output=False
)
print("Shape de la mascara:", mask.shape)

# -- Calculamos propiedades del palo
# Punto inicial y final para interpolar la recta
x1 = 10; x2 = mask.shape[1]-x1
first_colum = mask[:, 10]
last_colum = mask[:, x2]
y1 = np.where(first_colum == 1)[0][0]
y2 = np.where(last_colum == 1)[0][0]
p1 = (x1,y1); p2 = (x2,y2)
print("Punto 1", p1, "| Punto 2", p2)
# Anchura en pixeles
width1 = np.where(first_colum[y1+1:] == 0)[0][0]
width2 = np.where(last_colum[y2+1:] == 0)[0][0]
stick_width = round((width1+width2)/2)
print("Anchura del palo (pixeles):", stick_width)

plt.subplot(rows,colums,2)
plt.title("Segmentacion del Palo")
plt.imshow(mask, cmap='gray')

# -- Calculamos la recta y la aplicamos sobre las imagenes
class Recta():
    
    def __init__(self, p1:tuple, p2:tuple) -> None:
        x1, y1 = p1
        x2, y2 = p2
        m = (y2-y1)/(x2-x1); n = y1 - (x1*m)
        self.m = m
        self.n = n
    
    def get_y(self, x:np.ndarray):
        return np.around((x*self.m) + self.n).astype(np.uint16)
    
recta_umbral = Recta(p1,p2)

x_recta = np.arange(start=0, stop=mask.shape[1], step=1)
print("Recta Shape:", x_recta.shape)
assert x_recta.shape[0] == mask.shape[1]
y_recta1 = recta_umbral.get_y(x_recta)
y_recta2 = y_recta1+round(stick_width/2)

plt.subplot(rows,colums,3)
plt.title("Aplicando Recta calculada")
plt.imshow(img)
plt.scatter(x_recta, y_recta1, color='blue', s=20)
plt.scatter(x_recta, y_recta2, color='red', s=20)
plt.show()

# -- Extrapolamos rectas a la imagen original
x1_big = x_start + x1; y1_big = y_start + y1  
x2_big = x_start + x2; y2_big = y_start + y2
p1_big = (x1_big, y1_big); p2_big = (x2_big, y2_big)
recta_umbral_big = Recta(p1_big, p2_big)
x_recta_big = np.arange(start=0, stop=img_raw.shape[1], step=1)
y_recta_big1 = recta_umbral_big.get_y(x_recta_big)
y_recta_big2 = y_recta_big1+round(stick_width/2)
plt.title("Aplicando Rectas calculadas a la imagen original")
plt.imshow(img_raw)
plt.scatter(x_recta_big, y_recta_big1, color='blue', s=2) #top
plt.scatter(x_recta_big, y_recta_big2, color='red', s=2) #bottom
plt.show()

def top():
    #top = np.array([x_recta_big],[y_recta_big1])
    m_top = Recta(p1_big, p2_big).m
    #n_top = Recta(p1_big, p2_big).n

    return(m_top)

def bottom():
    #bottom = np.array([x_recta_big],[y_recta_big2])
    #m_bottom = Recta(p1_big, p2_big).m
    n_bottom = Recta(p1_big, p2_big).n+round(stick_width/2)
    return(n_bottom)