#Miguel Rosas

# Verifica si se proporciona la cantidad_simulaciones como argumento
if [ $# -eq 0 ]; then
	echo "Uso: $0 cantidad_simulaciones"
	exit 1
fi

# Obtiene la cantidad_simulaciones desde el primer argumento
cantidad_simulaciones=$1

v1=0.01
v2=0.05
v3=0.1
v4=0.15
v5=0.25
v6=0.35
v7=0.45
v8=0.5

# Valores de Reynolds a utilizar
valores_v=("v1" "v2" "v3" "v4" "v5" "v6" "v7" "v8")

# Leer valores desde el archivo parametros.txt
nu=$(grep -oP 'nu\s*=\s*\K[\d.+-]+' parametros.txt)
Ld=$(grep -oP 'Ld\s*=\s*\K[\d.+-]+' parametros.txt)
Re=$(grep -oP 'Re\s*=\s*\K[\d.+-]+' parametros.txt)

lc=$(grep -oP 'lc\s*=\s*\K[\d.+-]+' parametros.txt)
rd=$(grep -oP 'rd\s*=\s*\K[\d.+-]+' parametros.txt)
l1=$(grep -oP 'l1\s*=\s*\K[\d.+-]+' parametros.txt)
a=$(grep -oP 'a\s*=\s*\K[\d.+-]+' parametros.txt)
rp=$(grep -oP 'rp\s*=\s*\K[\d.+-]+' parametros.txt)
np=$(grep -oP 'np\s*=\s*\K[\d.+-]+' parametros.txt)

tf=$(grep -oP 'tf\s*=\s*\K[\d.+-]+' parametros.txt)
dt=$(grep -oP 'dt\s*=\s*\K[\d.+-]+' parametros.txt)
wi=$(grep -oP 'wi\s*=\s*\K[\d.+-]+' parametros.txt)

# Bucle para crear y mover carpetas, editar y genrar mallado
for ((i = 1; i <= $cantidad_simulaciones; i++)); do
	# Genera el nombre de la carpeta
	carpeta_caso_i="Case_$i"

	# Crea la carpeta del caso
	mkdir "$carpeta_caso_i"

	# Copia carpetas del caso dentro de las carpetasgeneradas
	cp -r "Case_0/0/" "$carpeta_caso_i/"
	cp -r "Case_0/constant/" "$carpeta_caso_i/"
	cp -r "Case_0/system/" "$carpeta_caso_i/"
	cp -r "Case_0/geometry_script/" "$carpeta_caso_i/"
	cp "Case_0/mesh.geo" "$carpeta_caso_i/"
	cp "Scripts/graficar_p.py" "$carpeta_caso_i"
	cp "Scripts/graficar_vel.py" "$carpeta_caso_i"
	cp "Scripts/ajuste.py" "$carpeta_caso_i"
	cp "Scripts/extractor_p.py" "$carpeta_caso_i"
	cp "Scripts/extractor_p.sh" "$carpeta_caso_i"
	cp "Scripts/extractor_vel.py" "$carpeta_caso_i"
	cp "Scripts/extractor_vel.sh" "$carpeta_caso_i"

	cd "$carpeta_caso_i/"

	# Reemplazar valores en sus respectivos archivos
	sed -i "s/\$nuu/$nu/g" ./0/U
	sed -i "s/\$Ree/$Re/g" ./0/U
	sed -i "s/\$nuu/$nu/g" ./constant/transportProperties
	sed -i "s/\$LL/$Ld/g" ./0/U

	sed -i "s/\$rdd/$rd/g" ./mesh.geo
	sed -i "s/\$l11/$l1/g" ./mesh.geo
	sed -i "s/\$aa/$a/g" ./mesh.geo
	sed -i "s/\$lccc/$lc/g" ./mesh.geo

	sed -i "s/\$rdd/$rd/g" ./geometry_script/geometry.geo
	sed -i "s/\$l11/$l1/g" ./geometry_script/geometry.geo
	sed -i "s/\$aa/$a/g" ./geometry_script/geometry.geo
	sed -i "s/\$rpp/$rp/g" ./geometry_script/geometry.geo

	sed -i "s/\$npp/$np/g" ./geometry_script/generator_point_process.py
	sed -i "s/\$rpp/$rp/g" ./geometry_script/generator_point_process.py
	sed -i "s/\$rdd/$rd/g" ./geometry_script/generator_point_process.py

	sed -i "s/\$wii/$wi/g" ./system/controlDict
	sed -i "s/\$dtt/$dt/g" ./system/controlDict
	sed -i "s/\$tff/$tf/g" ./system/controlDict

	sed -i "s/\$ii/$i/g" ./extractor_p.py
	sed -i "s/\$ii/$i/g" ./extractor_vel.py

	mkdir Case_0
	mv 0/ Case_0/
	mv constant/ Case_0/
	mv system/ Case_0/
	mv geometry_script/ Case_0/
	mv mesh.geo Case_0/
	cd "./Case_0/"
	cd "./geometry_script/"
	#Generar mallado gmsh
	python3 generator_point_process.py
	./generate.sh
	cd ../..

	# Se inicia el ciclo para variar el valor de lc
	for j in {0..7}; do
		#se genera contador k
		k=$((j + 1))

		# se crea carpeta del caso para el valor de Reynolds
		carpeta_v="Case_${i}_${valores_v[$j]}"
		mkdir "$carpeta_v"

		#se copian los archivos a la carpeta del caso
		cp -r Case_0/0/ "$carpeta_v/"
		cp -r Case_0/constant/ "$carpeta_v/"
		cp -r Case_0/system/ "$carpeta_v/"
		cp -r Case_0/geometry_script/ "$carpeta_v/"
		cp Case_0/mesh.geo "$carpeta_v/"

		#Se reemplaza el valor de v en el archivo 0/U
		sed -i "s/\$vv/${!valores_v[$j]}/g" "$carpeta_v/0/U"

		cd "$carpeta_v/"
		touch "${valores_v[$j]}.foam"
		gmsh "./mesh.geo" -3
		#Genera mallado OpenFoam
		gmshToFoam "mesh.msh"

		# Utiliza grep para eliminar las líneas que contienen la palabra "physicalType" y sobrescribe el archivo original
		grep -v "physicalType" constant/polyMesh/boundary >constant/polyMesh/boundary.temp
		mv constant/polyMesh/boundary.temp constant/polyMesh/boundary

		# Reemplaza "patch" por "wall" en las líneas 23
		sed -i '23s/patch/wall/;' "constant/polyMesh/boundary"

		decomposePar
		mpirun -np 8 simpleFoam -parallel
		cd ..
	done
	kitty --hold -e bash -c "./extractor_p.sh && ./extractor_vel.sh ; exec bash" &
	cd ..
done

echo "Proceso completado."
