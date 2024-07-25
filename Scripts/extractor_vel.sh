# Lista de valores para v
valores_v=("v1" "v2" "v3" "v4" "v5" "v6" "v7" "v8")
for j in {0..7}; do
	# Crear un archivo temporal para el script modificado
	temp_script="temp_script_${valores_v[$j]}.py"

	# Copia el script original a un script temporal
	cp extract_vel.py $temp_script

	# Usa sed para reemplazar '$p' en el script temporal con el valor actual de p
	sed -i "s/\$jj/${valores_v[$j]}/g" $temp_script

	# Ejecuta el script Python modificado
	pvpython $temp_script

	# Opcional: Eliminar el script temporal después de la ejecución
	rm $temp_script

	# Opcional: Añadir otros comandos aquí si es necesario
done
