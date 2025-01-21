create database TiendaLibrosVac2025;
use TiendaLibrosVac2025;

-- Tabla para libros

create table Libros (
    ISBN VARCHAR(13) Primary key,
	titulo VARCHAR(255) not null,
	precio_compra DECIMAL(10,2) not null,
	precio_venta DECIMAL(10,2) not null,
	cantidad_actual INT NOT NULL default 0,
    CONSTRAINT chk_precios CHECK (precio_venta >= precio_compra),
    CONSTRAINT chk_cantidad CHECK (cantidad_actual >= 0)
);

-- Tabla para tipos de transacciones

create table TiposTransaccion (
    id_tipo INT primary key,
    nombre VARCHAR(50) not null,
    CONSTRAINT chk_tipo CHECK (nombre IN ('VENTA', 'ABASTECIMIENTO'))
);

-- Insertar tipos de transacciones válidos

INSERT INTO TiposTransaccion (id_tipo, nombre) VALUES 
(1, 'VENTA'),
(2, 'ABASTECIMIENTO');

-- Tabla para transacciones

create table Transacciones (
    id_transaccion INT identity (1,1) primary key,
    ISBN varchar(13) not null,
    tipo_transaccion INT not null,
    fecha_transaccion DATETIME not null default GETDATE(),
    cantidad INT NOT NULL,
    FOREIGN KEY (ISBN) REFERENCES Libros (ISBN) ON delete CASCADE,
    FOREIGN KEY (tipo_transaccion) REFERENCES TiposTransaccion (id_tipo),
    CONSTRAINT chk_cantidad_transaccion CHECK (cantidad > 0)
);

-- Tabla para caja

create table Caja (
    id_movimiento int IDENTITY(1,1) primary key,
    fecha_movimiento DATETIME not null default GETDATE(),
    tipo_movimiento VARCHAR(20) NOT NULL,
    monto DECIMAL(10,2) NOT NULL,
    saldo_actual DECIMAL(10,2) not null,
    id_transaccion INT,
    FOREIGN KEY (id_transaccion) REFERENCES Transacciones (id_transaccion),
    CONSTRAINT chk_tipo_movimiento CHECK (tipo_movimiento IN ('INGRESO', 'EGRESO'))
);

-- Ingresar el saldo inicial en la caja

INSERT INTO Caja (tipo_movimiento, monto, saldo_actual) VALUES ('INGRESO', 1000000.00, 1000000.00);
GO

-- Trigger para ventas: actualizar el inventario y la caja 

CREATE TRIGGER trg_Venta_Transaccion
ON Transacciones
AFTER INSERT
AS
BEGIN
    DECLARE @ISBN VARCHAR(13), @tipo_transaccion INT, @cantidad INT, @precio_venta DECIMAL(10,2);

    SELECT @ISBN = ISBN, @tipo_transaccion = tipo_transaccion, @cantidad = cantidad
    FROM inserted;
    
    IF @tipo_transaccion = 1
    BEGIN
        SELECT @precio_venta = precio_venta
        FROM Libros
        WHERE ISBN = @ISBN;

		-- Actualizar el inventario
		UPDATE Libros
		SET cantidad_actual = cantidad_actual - @cantidad
		WHERE ISBN = @ISBN;

		-- Actualizar la caja
		INSERT INTO Caja (tipo_movimiento, monto, saldo_actual, id_transaccion)    

		SELECT 'INGRESO', @cantidad * @precio_venta,
            (SELECT TOP 1 saldo_actual FROM Caja ORDER BY id_movimiento DESC)+ (@cantidad* @precio_venta),
            inserted.id_transaccion
		FROM inserted;
    END; 
END;

GO
-- Trigger para el abastecimiento de libros: actualizar inventario, restar dinero a la caja

CREATE TRIGGER trg_Abastecimiento_Transaccion
ON Transacciones
AFTER INSERT
AS
BEGIN
	DECLARE @ISBN VARCHAR(13), @tipo_transaccion INT, @cantidad INT, @precio_compra DECIMAL(10,2);

	IF @tipo_transaccion = 2
	BEGIN
		SELECT @precio_compra = precio_compra FROM Libros WHERE ISBN = @ISBN;

		-- Actualizar el inventario
		UPDATE Libros
		SET cantidad_actual = cantidad_actual + @cantidad
		WHERE ISBN = @ISBN;

		-- Registrar egreso en la caja
		INSERT INTO Caja (tipo_movimiento, monto, saldo_actual, id_transaccion)

		SELECT 'EGRESO', @cantidad * @precio_compra, 
            (SELECT TOP 1 saldo_actual FROM Caja ORDER BY id_movimiento DESC) - (@cantidad * @precio_compra),
            inserted.id_transaccion
		FROM inserted;
	END
END;