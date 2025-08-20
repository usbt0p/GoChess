- Mantener el código simple y directo. Mejor que se pueda entender rápidamente sin necesidad de comentarios extensos.

- No usar comentarios innecesarios o redundantes. Ejemplo:
    ```python
    def place_piece(self, piece: Piece, position: Position):
        """Places a piece on the board."""
        ...
    ```
    Pero comentarios explicando partes clave / poco legibles / complicadas del código son bienvenidos.

- Otros comentarios útiles son aquellos que explican el propósito de una función, clase o módulo, en lugar de su implementación o funcionamiento interno. Para eso ya está el código (asumiendo que está bien escrito y es legible). 

    Los todo's, fixme's y similares son bienvenidos, pero no abuses de ellos. Si un comentario es necesario, es mejor que el código sea refactorizado para que no lo necesite.

- Menos líneas no es necesariemente mejor. Del mismo modo, más líneas no es necesariamente peor. El equilibrio entre código conciso y legible es clave. Usa enters para separar "fases" distintas del código incluso dentro de una función / módilo, pero no abuses de ellos. 
Tampoco abuses de azucar sintáctico como comprehensions / oneliners si no son necesarias o excesivamente largas / complejas.

- Sigue las convenciones de estilo de Python (PEP 8). Para formato, cíñete al formato de black. Escribe el código en inglés.

- No te excedas en la implementación: si tienes una guía de lo que debes implementar y como, sigue esa guía. No añadas funcionalidades que no estén en la guía, a menos que sean necesarias para el funcionamiento del código. Si alguna implementación extra es necesaria, infórmame.