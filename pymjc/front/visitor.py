from __future__ import annotations
from abc import ABC, abstractmethod
import enum

from pymjc.front.ast import *
from pymjc.front.symbol import *

class SemanticErrorType(enum.Enum):
    ALREADY_DECLARED_CLASS = 1
    ALREADY_DECLARED_METHOD = 2
    ALREADY_DECLARED_VAR = 3
    AND_TYPE_MISMATCH = 4
    ARG_TYPE_MISMATCH = 5
    ARRAY_ASSIGN_TYPE_MISMATCH = 6
    ARRAY_LENGTH_TYPE_MISMATCH = 7
    ARRAY_TYPE_MISMATCH = 8
    ASSIGN_TYPE_MISMATCH = 9
    DUPLICATED_ARG = 10
    IF_TYPE_MISMATCH = 11
    INDEX_TYPE_MISMATCH = 12
    INVALID_OBJECT_IDENTIFIER = 13
    LESS_THAN_TYPE_MISMATCH = 14
    MINUS_TYPE_MISMATCH = 15
    NEW_ARRAY_TYPE_MISMATCH = 16
    NEW_OBJECT_UNDECLARED_CLASS = 17
    NOT_TYPE_MISMATCH = 18
    PLUS_TYPE_MISMATCH = 19
    RETURN_TYPE_MISMATCH = 20
    TIMES_TYPE_MISMATCH = 21
    UNDECLARED_CLASS = 22
    UNDECLARED_IDENTIFIER = 23
    UNDECLARED_METHOD = 24
    UNDECLARED_SUPER_CLASS = 25 
    WHILE_TYPE_MISMATCH = 26
    WRONG_ARG_NUMBER = 27

########################################
# AST Simple Visitors
########################################

class Visitor(ABC):

    @abstractmethod
    def visit_program(self, element: Program) -> None:
        pass

    @abstractmethod
    def visit_main_class(self, element: MainClass) -> None:
        pass

    @abstractmethod
    def visit_class_decl_extends(self, element: ClassDeclExtends) -> None:
        pass

    @abstractmethod
    def visit_class_decl_simple(self, element: ClassDeclSimple) -> None:
        pass

    @abstractmethod
    def visit_var_decl(self, element: VarDecl) -> None:
        pass
  
    @abstractmethod
    def visit_method_decl(self, element: MethodDecl) -> None:
        pass

    @abstractmethod
    def visit_formal(self, element: Formal) -> None:
        pass

    @abstractmethod
    def visit_int_array_type(self, element: IntArrayType) -> None:
        pass

    @abstractmethod
    def visit_boolean_type(self, element: BooleanType) -> None:
        pass

    @abstractmethod
    def visit_integer_type(self, element: IntegerType) -> None:
        pass

    @abstractmethod
    def visit_identifier_type(self, element: IdentifierType) -> None:
        pass

    @abstractmethod
    def visit_block(self, element: Block) -> None:
        pass

    @abstractmethod
    def visit_if(self, element: If) -> None:
        pass
  
    @abstractmethod
    def visit_while(self, element: While) -> None:
        pass

    @abstractmethod
    def visit_print(self, element: Print) -> None:
        pass

    @abstractmethod
    def visit_assign(self, element: Assign) -> None:
        pass

    @abstractmethod
    def visit_array_assign(self, element: ArrayAssign) -> None:
        pass

    @abstractmethod
    def visit_and(self, element: And) -> None:
        pass

    @abstractmethod
    def visit_less_than(self, element: LessThan) -> None:
        pass

    @abstractmethod
    def visit_plus(self, element: Plus) -> None:
        pass

    @abstractmethod
    def visit_minus(self, element: Minus) -> None:
        pass

    @abstractmethod
    def visit_times(self, element: Times) -> None:
        pass

    @abstractmethod
    def visit_array_lookup(self, element: ArrayLookup) -> None:
        pass

    @abstractmethod
    def visit_array_length(self, element: ArrayLength) -> None:
        pass

    @abstractmethod
    def visit_call(self, element: Call) -> None:
        pass

    @abstractmethod
    def visit_integer_literal(self, element: IntegerLiteral) -> None:
        pass

    @abstractmethod
    def visit_true_exp(self, element: TrueExp) -> None:
        pass

    @abstractmethod
    def visit_false_exp(self, element: FalseExp) -> None:
        pass

    @abstractmethod
    def visit_identifier_exp(self, element: IdentifierExp) -> None:
        pass

    @abstractmethod
    def visit_this(self, element: This) -> None:
        pass

    @abstractmethod
    def visit_new_array(self, element: NewArray) -> None:
        pass

    @abstractmethod
    def visit_new_object(self, element: NewObject) -> None:
        pass


    @abstractmethod
    def visit_not(self, element: Not) -> None:
        pass

    @abstractmethod
    def visit_identifier(self, element: Identifier) -> None:
        pass




class PrettyPrintVisitor(Visitor):

    def __init__(self) -> None:
        super().__init__()
        self.iden = 1

    def inc_iden(self) -> None:
        self.iden = self.iden + 1

    def dec_iden(self) -> None:
        self.iden = self.iden - 1

    def get_iden(self) -> str:
        return  " " * self.iden

    def visit_program(self, element: Program) -> None:
        element.main_class.accept(self)
        for index in range(element.class_decl_list.size()):
            print()
            element.class_decl_list.element_at(index).accept(self)

    def visit_main_class(self, element: MainClass) -> None:
        print("class", end=' ')
        element.class_name_identifier.accept(self)
        print(" {")
        print(self.get_iden(),"public static void main (String [] ", end=' ')
        element.arg_name_ideintifier.accept(self)
        print(") {")
        print()
        self.inc_iden()
        element.statement.accept(self)
        self.dec_iden()
        print()
        print(self.get_iden(), "}")
        print("}")

    def visit_class_decl_extends(self, element: ClassDeclExtends) -> None:
        print("class", end=' ')
        element.class_name.accept(self)
        print(" extends", end=' ')
        element.super_class_name.accept(self)
        print(" {")

        self.inc_iden()
        for index in range(element.var_decl_list.size()):
            #print(self.get_iden(), end='')
            element.var_decl_list.element_at(index).accept(self)
            if (index + 1 < element.var_decl_list.size() ): 
                print()
    
        for index in range(element.method_decl_list.size()):
            print()
            element.method_decl_list.element_at(index).accept(self)
        self.dec_iden()
        print()
        print("}")


    def visit_class_decl_simple(self, element: ClassDeclSimple) -> None:
        print("class", end=' ')
        element.class_name.accept(self)
        print(" {")

        self.inc_iden()
        for index in range(element.var_decl_list.size()):
            element.var_decl_list.element_at(index).accept(self)
            if (index + 1 < element.var_decl_list.size()): 
                print()
    
        for index in range(element.method_decl_list.size()):
            print()
            element.method_decl_list.element_at(index).accept(self)
            
        self.dec_iden()
        print()
        print("}")


    def visit_var_decl(self, element: VarDecl) -> None:
        print(self.get_iden(), end='')
        element.type.accept(self)
        print(" ", end='')
        element.name.accept(self)
        print(";")
     

    def visit_method_decl(self, element: MethodDecl) -> None:
        print(self.get_iden(), "public", end=' ')
        element.type.accept(self)
        print(" ", end='')
        element.name.accept(self)
        print(" (", end='')

        for index in range(element.formal_param_list.size()):
            element.formal_param_list.element_at(index).accept(self)
            if(index + 1 < element.formal_param_list.size()):
                print(", ", end='')
        
        print(") {")

        self.inc_iden()
        for index in range(element.var_decl_list.size()):
            #print(self.get_iden(), end='')
            element.var_decl_list.element_at(index).accept(self)
        
        for index in range(element.statement_list.size()):
            #print(self.get_iden(), end='')
            element.statement_list.element_at(index).accept(self)
            if(index + 1 < element.statement_list.size()):
                print()

        print(self.get_iden(), "return ", end='')
        element.return_exp.accept(self)
        print(";")
        self.dec_iden()
        print(self.get_iden(), "}")


    def visit_formal(self, element: Formal) -> None:
        element.type.accept(self)
        print(" ", end='')
        element.name.accept(self)


    def visit_int_array_type(self, element: IntArrayType) -> None:
        print("int []", end='')

    
    def visit_boolean_type(self, element: BooleanType) -> None:
        print("boolean", end='')

    
    def visit_integer_type(self, element: IntegerType) -> None:
        print("int", end='')

    
    def visit_identifier_type(self, element: IdentifierType) -> None:
        print(element.name, end='')

    
    def visit_block(self, element: Block) -> None:
        print(self.get_iden(),"{ ")
        self.inc_iden()
        for index in range(element.statement_list.size()):
            print(self.get_iden(), end='')
            element.statement_list.element_at(index).accept(self)
            print()

        self.dec_iden()
        print(self.get_iden(), "} ")

    def visit_if(self, element: If) -> None:
        print(self.get_iden(), "if (", end='')
        element.condition_exp.accept(self)
        print(")")
        self.inc_iden()
        element.if_statement.accept(self)
        self.dec_iden()
        print()
        print(self.get_iden(), "else")
        self.inc_iden()
        element.else_statement.accept(self)
        self.dec_iden()
  

    def visit_while(self, element: While) -> None:
        print(self.get_iden(),"while (", end='')
        element.condition_exp.accept(self)
        print(")")
        self.inc_iden()
        element.statement.accept(self)
        self.dec_iden()

    
    def visit_print(self, element: Print) -> None:
        print(self.get_iden(), "System.out.println(", end='')
        element.print_exp.accept(self)
        print(");", end='')


    def visit_assign(self, element: Assign) -> None:
        print(self.get_iden(), end='')
        element.left_side.accept(self)
        print(" = ", end='')
        element.right_side.accept(self)
        print(";", end='')

    
    def visit_array_assign(self, element: ArrayAssign) -> None:
        print(self.get_iden(), end='')
        element.array_name.accept(self)
        print("[", end='')
        element.array_exp.accept(self)
        print("] = ", end='')
        element.right_side.accept(self)
        print(";", end='')

    
    def visit_and(self, element: And) -> None:
        print("(", end='')
        element.left_side.accept(self)
        print(" && ", end='')
        element.right_side.accept(self)
        print(")", end='')

    def visit_less_than(self, element: LessThan) -> None:
        print("(", end='')
        element.left_side.accept(self)
        print(" < ", end='')
        element.right_side.accept(self)
        print(")", end='')


    def visit_plus(self, element: Plus) -> None:
        print("(", end='')
        element.left_side.accept(self)
        print(" + ", end='')
        element.right_side.accept(self)
        print(")", end='')


    def visit_minus(self, element: Minus) -> None:
        print("(", end='')
        element.left_side.accept(self)
        print(" - ", end='')
        element.right_side.accept(self)
        print(")", end='')

    
    def visit_times(self, element: Times) -> None:
        print("(", end='')
        element.left_side.accept(self)
        print(" * ", end='')
        element.right_side.accept(self)
        print(")", end='')


    def visit_array_lookup(self, element: ArrayLookup) -> None:
        element.out_side_exp.accept(self)
        print("[", end='')
        element.in_side_exp.accept(self)
        print("]", end='')

    def visit_array_length(self, element: ArrayLength) -> None:
        element.length_exp.accept(self)
        print(".length", end='')


    def visit_call(self, element: Call) -> None:
        element.callee_exp.accept(self)
        print(".", end='')
        element.callee_name.accept(self)
        print("(", end='')
        for index in range(element.arg_list.size()):
            element.arg_list.element_at(index).accept(self)
            if( index + 1 < element.arg_list.size()):
                print(", ", end='')
        print(")", end='')


    def visit_integer_literal(self, element: IntegerLiteral) -> None:
        print(element.value, end='')


    def visit_true_exp(self, element: TrueExp) -> None:
        print("true", end='')


    def visit_false_exp(self, element: FalseExp) -> None:
        print("false", end='')


    def visit_identifier_exp(self, element: IdentifierExp) -> None:
        print(element.name, end='')

    def visit_this(self, element: This) -> None:
        print("this", end='')

    def visit_new_array(self, element: NewArray) -> None:
        print("new int[", end='') 
        element.new_exp.accept(self)
        print("]", end='')


    def visit_new_object(self, element: NewObject) -> None:
        print("new ", end='')
        element.object_name.accept(self)
        print("()", end='')


    def visit_not(self, element: Not) -> None:
        print("!", end='')
        element.negated_exp.accept(self)


    def visit_identifier(self, element: Identifier) -> None:
        print(element.name, end='')
    


class DepthFirstVisitor(Visitor):

    def visit_program(self, element: Program) -> None:
        element.main_class.accept(self)
        for index in range(element.class_decl_list.size()):
            element.class_decl_list.element_at(index).accept(self)

    def visit_main_class(self, element: MainClass) -> None:
        element.class_name_identifier.accept(self)
        element.arg_name_ideintifier.accept(self)
        element.statement.accept(self)

    def visit_class_decl_extends(self, element: ClassDeclExtends) -> None:
        element.class_name.accept(self)
        element.super_class_name.accept(self)
        for index in range(element.var_decl_list.size()):
            element.var_decl_list.element_at(index).accept(self)
    
        for index in range(element.method_decl_list.size()):
            element.method_decl_list.element_at(index).accept(self)


    def visit_class_decl_simple(self, element: ClassDeclSimple) -> None:
        element.class_name.accept(self)

        for index in range(element.var_decl_list.size()):
            element.var_decl_list.element_at(index).accept(self)
    
        for index in range(element.method_decl_list.size()):
            element.method_decl_list.element_at(index).accept(self)


    def visit_var_decl(self, element: VarDecl) -> None:
        element.type.accept(self)
        element.name.accept(self)
     

    def visit_method_decl(self, element: MethodDecl) -> None:
        element.type.accept(self)
        element.name.accept(self)

        for index in range(element.formal_param_list.size()):
            element.formal_param_list.element_at(index).accept(self)

        for index in range(element.var_decl_list.size()):
            element.var_decl_list.element_at(index).accept(self)

        for index in range(element.statement_list.size()):
            element.statement_list.element_at(index).accept(self)

        element.return_exp.accept(self)


    def visit_formal(self, element: Formal) -> None:
        element.type.accept(self)
        element.type.accept(self)


    def visit_int_array_type(self, element: IntArrayType) -> None:
        return None
    
    def visit_boolean_type(self, element: BooleanType) -> None:
        return None
    
    def visit_integer_type(self, element: IntegerType) -> None:
        return None

    def visit_identifier_type(self, element: IdentifierType) -> None:
        return None

    
    def visit_block(self, element: Block) -> None:
        for index in range(element.statement_list.size()):
            element.statement_list.element_at(index).accept(self)

    def visit_if(self, element: If) -> None:
        element.condition_exp.accept(self)
        element.if_statement.accept(self)
        element.else_statement.accept(self)
  

    def visit_while(self, element: While) -> None:
        element.condition_exp.accept(self)
        element.statement.accept(self)

    
    def visit_print(self, element: Print) -> None:
        element.print_exp.accept(self)

    def visit_assign(self, element: Assign) -> None:
        element.left_side.accept(self)
        element.right_side.accept(self)

    
    def visit_array_assign(self, element: ArrayAssign) -> None:
        element.array_name.accept(self)
        element.array_exp.accept(self)
        element.right_side.accept(self)

    
    def visit_and(self, element: And) -> None:
        element.left_side.accept(self)
        element.right_side.accept(self)

    def visit_less_than(self, element: LessThan) -> None:
        element.left_side.accept(self)
        element.right_side.accept(self)


    def visit_plus(self, element: Plus) -> None:
        element.left_side.accept(self)
        element.right_side.accept(self)


    def visit_minus(self, element: Minus) -> None:
        element.left_side.accept(self)
        element.right_side.accept(self)

    
    def visit_times(self, element: Times) -> None:
        element.left_side.accept(self)
        element.right_side.accept(self)


    def visit_array_lookup(self, element: ArrayLookup) -> None:
        element.out_side_exp.accept(self)
        element.in_side_exp.accept(self)

    def visit_array_length(self, element: ArrayLength) -> None:
        element.length_exp.accept(self)



    def visit_call(self, element: Call) -> None:
        element.callee_exp.accept(self)
        element.callee_name.accept(self)
        for index in range(element.arg_list.size()):
            element.arg_list.element_at(index).accept(self)


    def visit_integer_literal(self, element: IntegerLiteral) -> None:
        return None


    def visit_true_exp(self, element: TrueExp) -> None:
        return None


    def visit_false_exp(self, element: FalseExp) -> None:
        return None


    def visit_identifier_exp(self, element: IdentifierExp) -> None:
        return None

    def visit_this(self, element: This) -> None:
        return None

    def visit_new_array(self, element: NewArray) -> None:
        element.new_exp.accept(self)


    def visit_new_object(self, element: NewObject) -> None:
        element.object_name.accept(self)


    def visit_not(self, element: Not) -> None:
        element.negated_exp.accept(self)


    def visit_identifier(self, element: Identifier) -> None:
        return None


#TODO
class FillSymbolTableVisitor(Visitor):
    def __init__(self) -> None:
        super().__init__()
        self.semantic_errors = {}
        self.symbol_table = SymbolTable()
        self.src_file_name = "UnknownSRCFile"

    def init_semantic_errors(self) -> None:
        for error_type in SemanticErrorType:
            self.semantic_errors[error_type.name] = 0

    def fill_semantic_errors(self, semantic_errors) -> None:
            self.semantic_errors = semantic_errors

    def add_semantic_error(self, error_type: SemanticErrorType) -> None:
            self.semantic_errors[error_type.name] += 1

    def get_symbol_table(self) -> SymbolTable:
        return self.symbol_table

    def visit_program(self, element: Program) -> None:
        element.main_class.accept(self)

        for index in range(element.class_decl_list.size()):
            element.class_decl_list.element_at(index).accept(self)

    def visit_main_class(self, element: MainClass) -> None:
        element.class_name_identifier.accept(self)
        self.symbol_table.add_scope(element.class_name_identifier, ClassEntry())

        element.arg_name_ideintifier.accept(self)
        
        element.statement.accept(self)


    def visit_class_decl_extends(self, element: ClassDeclExtends) -> None:
        element.class_name.accept(self)
        if not self.symbol_table.add_scope(element.class_name, ClassEntry()):
            self.add_semantic_error(SemanticErrorType.ALREADY_DECLARED_CLASS)
            
        element.super_class_name.accept(self)
        if not self.symbol_table.contains_key(element.super_class_name):
            self.add_semantic_error(SemanticErrorType.UNDECLARED_SUPER_CLASS)
        
        self.symbol_table.add_extends_entry(element.class_name, element.super_class_name)

        for index in range(element.var_decl_list.size()):
            current = element.var_decl_list.element_at(index)
            current.accept(self)
            #if not self.symbol_table.add_field(current):
            #    self.add_semantic_error(SemanticErrorType.ALREADY_DECLARED_VAR)

        for index in range(element.method_decl_list.size()):
            current = element.method_decl_list.element_at(index)
            current.accept(self)
            #if not self.symbol_table.add_field(current):
            #    self.add_semantic_error(SemanticErrorType.ALREADY_DECLARED_METHOD)
   #alerta: checar se class_name deve ser accepted antes ou depois
    def visit_class_decl_simple(self, element: ClassDeclSimple) -> None:    
        element.class_name.accept(self)
        if not self.symbol_table.add_scope(element.class_name, ClassEntry()):
            self.add_semantic_error(SemanticErrorType.ALREADY_DECLARED_CLASS)
            
        for index in range(element.var_decl_list.size()):
            current = element.var_decl_list.element_at(index)
            current.accept(self)
            if not self.symbol_table.add_field(current):
                self.add_semantic_error(SemanticErrorType.ALREADY_DECLARED_VAR)

        for index in range(element.method_decl_list.size()):
            current = element.method_decl_list.element_at(index)
            current.accept(self)
            if not self.symbol_table.add_field(current):
                self.add_semantic_error(SemanticErrorType.ALREADY_DECLARED_METHOD)

# alerta: implementação considerando que visit_id retorna none
    def visit_var_decl(self, element: VarDecl) -> None:
        element.type.accept(self)
        element.name.accept(self)
        # caso seja um campo da classe:
        if not self.symbol_table.curr_method:
          #tenta adicionar a variável:
            if not self.symbol_table.curr_class.add_var(element.name, element.type):
              self.add_semantic_error(SemanticErrorType.ALREADY_DECLARED_VAR)
        # caso seja uma var local de um metodo:
        elif not self.symbol_table.curr_method.add_local(element.name,element.type):
            # tenta adicionar a variável para o metodo:
            self.add_semantic_error(SemanticErrorType.ALREADY_DECLARED_VAR)

    def visit_method_decl(self, element: MethodDecl) -> None:
        element.type.accept(self)
        element.name.accept(self)
        #tenta adicionar ele:
        if not self.symbol_table.add_method(element.name, MethodEntry()):
            # erro caso não conseguir
            self.add_semantic_error(SemanticErrorType.ALREADY_DECLARED_METHOD)

        for index in range(element.formal_param_list.size()):
            element.formal_param_list.element_at(index).accept(self)

        for index in range(element.var_decl_list.size()):
            element.var_decl_list.element_at(index).accept(self)

        for index in range(element.statement_list.size()):
            element.statement_list.element_at(index).accept(self)

        element.return_exp.accept(self)

    def visit_formal(self, element: Formal) -> None:
        element.type.accept(self)
        element.name.accept(self)
        #tenta adicionar ele:
        if not self.symbol_table.curr_method.add_param(element.name, element.type):
            # erro caso não conseguir
            self.add_semantic_error(SemanticErrorType.DUPLICATED_ARG)


    def visit_int_array_type(self, element: IntArrayType) -> None:
        return None
    
    def visit_boolean_type(self, element: BooleanType) -> None:
        return None
    
    def visit_integer_type(self, element: IntegerType) -> None:
        return None
    #alerta:
    def visit_identifier_type(self, element: IdentifierType) -> None:
        element.name.accept(self)
        #self.curr_class.contains_field(element.name) # não sei se era pra ser aqui ou só no visit_identifier

    def visit_block(self, element: Block) -> None:
        for index in range(element.statement_list.size()):
            element.statement_list.element_at(index).accept(self)

    def visit_if(self, element: If) -> None:
        element.condition_exp.accept(self)
        element.if_statement.accept(self)
        element.else_statement.accept(self)
  
    def visit_while(self, element: While) -> None:
        element.condition_exp.accept(self)
        element.statement.accept(self)

    def visit_print(self, element: Print) -> None:
        element.print_exp.accept(self)

    def visit_assign(self, element: Assign) -> None:
        element.left_side.accept(self)
        element.right_side.accept(self)
        # lado esquerdo:
        # caso seja um campo da classe:
        if not self.symbol_table.curr_method:
            if not self.symbol_table_curr_class.contains_field(element.left_side):
                self.add_semantic_error(SemanticErrorType.UNDECLARED_IDENTIFIER)
        # se for um campo de método:
        elif not self.symbol_table_curr_method.contains_local(element.left_side): 
            self.add_semantic_error(SemanticErrorType.UNDECLARED_IDENTIFIER)
        # lado direito: 
        # caso não for um 
        

    def visit_array_assign(self, element: ArrayAssign) -> None:
        element.array_name.accept(self)
        element.array_exp.accept(self)
        element.right_side.accept(self)
    
    def visit_and(self, element: And) -> None:
        element.left_side.accept(self)
        element.right_side.accept(self)

    def visit_less_than(self, element: LessThan) -> None:
        element.left_side.accept(self)
        element.right_side.accept(self)

    def visit_plus(self, element: Plus) -> None:
        element.left_side.accept(self)
        element.right_side.accept(self)

    def visit_minus(self, element: Minus) -> None:
        element.left_side.accept(self)
        element.right_side.accept(self)

    def visit_times(self, element: Times) -> None:
        element.left_side.accept(self)
        element.right_side.accept(self)

    def visit_array_lookup(self, element: ArrayLookup) -> None:
        element.out_side_exp.accept(self)
        element.in_side_exp.accept(self)

    def visit_array_length(self, element: ArrayLength) -> None:
        element.length_exp.accept(self)

    def visit_call(self, element: Call) -> None:
        element.callee_exp.accept(self)
        element.callee_name.accept(self)
        for index in range(element.arg_list.size()):
            element.arg_list.element_at(index).accept(self)
            if len(element.arg_list) != self.symbol_table.get_method(element.callee_name).get_num_params():
              self.add_semantic_error(WRONG_ARG_NUMBER)  

    def visit_integer_literal(self, element: IntegerLiteral) -> None:
        return None


    def visit_true_exp(self, element: TrueExp) -> None:
        return None

    def visit_false_exp(self, element: FalseExp) -> None:
        return None

    def visit_identifier_exp(self, element: IdentifierExp) -> None:
        if not self.curr_class.contains_field(element.name) or not self.curr_method.contains_local(element.name):
          self.add_semantic_error(SemanticErrorType.UNDECLARED_IDENTIFIER)
        #return None

    def visit_this(self, element: This) -> None:
        return None

    def visit_new_array(self, element: NewArray) -> None:
        element.new_exp.accept(self)

    def visit_new_object(self, element: NewObject) -> None:
        element.object_name.accept(self)
        if not self.symbol_table.get_class_entry(element.object_name):
            self.add_semantic_error(SemanticErrorType.NEW_OBJECT_UNDECLARED_CLASS)

    def visit_not(self, element: Not) -> None:
        element.negated_exp.accept(self)

    def visit_identifier(self, element: Identifier) -> None:
        return None

# importante:
# - deve-se provavelmente tirar o accept de nomes de classes e metodos em alguns casos (tomar cuidado pra nao procurar algo antes dele ser criado) 
# - checar se o visitor_identifier é pra checar se JÁ tem ou NÃO tem o id 



########################################
# AST Type Visitors
########################################
class TypeVisitor(ABC):

    @abstractmethod
    def visit_program(self, element: Program) -> Type:
        pass

    @abstractmethod
    def visit_main_class(self, element: MainClass) -> Type:
        pass

    @abstractmethod
    def visit_class_decl_extends(self, element: ClassDeclExtends) -> Type:
        pass

    @abstractmethod
    def visit_class_decl_simple(self, element: ClassDeclSimple) -> Type:
        pass

    @abstractmethod
    def visit_var_decl(self, element: VarDecl) -> Type:
        pass
  
    @abstractmethod
    def visit_method_decl(self, element: MethodDecl) -> Type:
        pass

    @abstractmethod
    def visit_formal(self, element: Formal) -> Type:
        pass

    @abstractmethod
    def visit_int_array_type(self, element: IntArrayType) -> Type:
        pass

    @abstractmethod
    def visit_boolean_type(self, element: BooleanType) -> Type:
        pass

    @abstractmethod
    def visit_integer_type(self, element: IntegerType) -> Type:
        pass

    @abstractmethod
    def visit_identifier_type(self, element: IdentifierType) -> Type:
        pass

    @abstractmethod
    def visit_block(self, element: Block) -> Type:
        pass

    @abstractmethod
    def visit_if(self, element: If) -> Type:
        pass
  
    @abstractmethod
    def visit_while(self, element: While) -> Type:
        pass

    @abstractmethod
    def visit_print(self, element: Print) -> Type:
        pass

    @abstractmethod
    def visit_assign(self, element: Assign) -> Type:
        pass

    @abstractmethod
    def visit_array_assign(self, element: ArrayAssign) -> Type:
        pass

    @abstractmethod
    def visit_and(self, element: And) -> Type:
        pass

    @abstractmethod
    def visit_less_than(self, element: LessThan) -> Type:
        pass

    @abstractmethod
    def visit_plus(self, element: Plus) -> Type:
        pass

    @abstractmethod
    def visit_minus(self, element: Minus) -> Type:
        pass

    @abstractmethod
    def visit_times(self, element: Times) -> Type:
        pass

    @abstractmethod
    def visit_array_lookup(self, element: ArrayLookup) -> Type:
        pass

    @abstractmethod
    def visit_array_length(self, element: ArrayLength) -> Type:
        pass

    @abstractmethod
    def visit_call(self, element: Call) -> Type:
        pass

    @abstractmethod
    def visit_integer_literal(self, element: IntegerLiteral) -> Type:
        pass

    @abstractmethod
    def visit_true_exp(self, element: TrueExp) -> Type:
        pass

    @abstractmethod
    def visit_false_exp(self, element: FalseExp) -> Type:
        pass

    @abstractmethod
    def visit_identifier_exp(self, element: IdentifierExp) -> Type:
        pass

    @abstractmethod
    def visit_this(self, element: This) -> Type:
        pass

    @abstractmethod
    def visit_new_array(self, element: NewArray) -> Type:
        pass

    @abstractmethod
    def visit_new_object(self, element: NewObject) -> Type:
        pass


    @abstractmethod
    def visit_not(self, element: Not) -> Type:
        pass

    @abstractmethod
    def visit_identifier(self, element: Identifier) -> Type:
        pass



class TypeDepthFirstVisitor(TypeVisitor):

    def visit_program(self, element: Program) -> Type:
        element.main_class.accept_type(self)
        for index in range(element.class_decl_list.size()):
            element.class_decl_list.element_at(index).accept_type(self)
        return None

    def visit_main_class(self, element: MainClass) -> Type:
        element.class_name_identifier.accept_type(self)
        element.arg_name_ideintifier.accept_type(self)
        element.statement.accept_type(self)
        return None

    def visit_class_decl_extends(self, element: ClassDeclExtends) -> Type:
        element.class_name.accept_type(self)
        element.super_class_name.accept_type(self)
        for index in range(element.var_decl_list.size()):
            element.var_decl_list.element_at(index).accept_type(self)
    
        for index in range(element.method_decl_list.size()):
            element.method_decl_list.element_at(index).accept_type(self)

        return None    

    def visit_class_decl_simple(self, element: ClassDeclSimple) -> Type:
        element.class_name.accept_type(self)

        for index in range(element.var_decl_list.size()):
            element.var_decl_list.element_at(index).accept_type(self)
    
        for index in range(element.method_decl_list.size()):
            element.method_decl_list.element_at(index).accept_type(self)
        
        return None

    def visit_var_decl(self, element: VarDecl) -> Type:
        element.type.accept_type(self)
        element.name.accept_type(self)
        return None
     

    def visit_method_decl(self, element: MethodDecl) -> Type:
        element.type.accept_type(self)
        element.name.accept_type(self)

        for index in range(element.formal_param_list.size()):
            element.formal_param_list.element_at(index).accept_type(self)

        for index in range(element.var_decl_list.size()):
            element.var_decl_list.element_at(index).accept_type(self)

        for index in range(element.statement_list.size()):
            element.statement_list.element_at(index).accept_type(self)

        element.return_exp.accept_type(self)
        return None


    def visit_formal(self, element: Formal) -> Type:
        element.type.accept_type(self)
        element.type.accept_type(self)
        return None


    def visit_int_array_type(self, element: IntArrayType) -> Type:
        return None
    
    def visit_boolean_type(self, element: BooleanType) -> Type:
        return None
    
    def visit_integer_type(self, element: IntegerType) -> Type:
        return None

    
    def visit_identifier_type(self, element: IdentifierType) -> Type:
        return None

    
    def visit_block(self, element: Block) -> Type:
        for index in range(element.statement_list.size()):
            element.statement_list.element_at(index).accept_type(self)
        
        return None

    def visit_if(self, element: If) -> Type:
        element.condition_exp.accept_type(self)
        element.if_statement.accept_type(self)
        element.else_statement.accept_type(self)
        return None
  

    def visit_while(self, element: While) -> Type:
        element.condition_exp.accept_type(self)
        element.statement.accept_type(self)
        return None

    
    def visit_print(self, element: Print) -> Type:
        element.print_exp.accept_type(self)
        return None


    def visit_assign(self, element: Assign) -> Type:
        element.left_side.accept_type(self)
        element.right_side.accept_type(self)
        return None

    
    def visit_array_assign(self, element: ArrayAssign) -> Type:
        element.array_name.accept_type(self)
        element.array_exp.accept_type(self)
        element.right_side.accept_type(self)
        return None

    
    def visit_and(self, element: And) -> Type:
        element.left_side.accept_type(self) 
        element.right_side.accept_type(self)
        return None

    def visit_less_than(self, element: LessThan) -> Type:
        element.left_side.accept_type(self)
        element.right_side.accept_type(self)
        return None


    def visit_plus(self, element: Plus) -> Type:
        element.left_side.accept_type(self)
        element.right_side.accept_type(self)
        return None


    def visit_minus(self, element: Minus) -> Type:
        element.left_side.accept_type(self)
        element.right_side.accept_type(self)
        return None

    
    def visit_times(self, element: Times) -> Type:
        element.left_side.accept_type(self)
        element.right_side.accept_type(self)
        return None


    def visit_array_lookup(self, element: ArrayLookup) -> Type:
        element.out_side_exp.accept_type(self)
        element.in_side_exp.accept_type(self)
        return None

    def visit_array_length(self, element: ArrayLength) -> Type:
        element.length_exp.accept_type(self)
        return None


    def visit_call(self, element: Call) -> Type:
        element.callee_exp.accept_type(self)
        element.callee_name.accept_type(self)
        for index in range(element.arg_list.size()):
            element.arg_list.element_at(index).accept_type(self)
        return None


    def visit_integer_literal(self, element: IntegerLiteral) -> Type:
        return None


    def visit_true_exp(self, element: TrueExp) -> Type:
        return None


    def visit_false_exp(self, element: FalseExp) -> Type:
        return None


    def visit_identifier_exp(self, element: IdentifierExp) -> Type:
        return None


    def visit_this(self, element: This) -> Type:
        return None


    def visit_new_array(self, element: NewArray) -> Type:
        element.new_exp.accept_type(self)
        return None


    def visit_new_object(self, element: NewObject) -> Type:
        element.object_name.accept_type(self)
        return None


    def visit_not(self, element: Not) -> Type:
        element.negated_exp.accept_type(self)
        return None


    def visit_identifier(self, element: Identifier) -> Type:
        return None



#TODO
class TypeCheckingVisitor(TypeVisitor): 
    def checkTypes(self, leftOp: Type, rightOp: Type, type: Type ):
      if type(leftOp)==type(Type) and type(rightOp)==type(Type):
        return True
      else:
        return False
    def visit_program(self, element: Program) -> Type:
        element.main_class.accept_type(self)
        for index in range(element.class_decl_list.size()):
            element.class_decl_list.element_at(index).accept_type(self)
        return None

    def visit_main_class(self, element: MainClass) -> Type:
        element.class_name_identifier.accept_type(self)
        element.arg_name_ideintifier.accept_type(self)
        element.statement.accept_type(self)
        return None

    def visit_class_decl_extends(self, element: ClassDeclExtends) -> Type:
        element.class_name.accept_type(self)
        element.super_class_name.accept_type(self)
        for index in range(element.var_decl_list.size()):
            element.var_decl_list.element_at(index).accept_type(self)
    
        for index in range(element.method_decl_list.size()):
            element.method_decl_list.element_at(index).accept_type(self)

        return None    

    def visit_class_decl_simple(self, element: ClassDeclSimple) -> Type:
        element.class_name.accept_type(self)

        for index in range(element.var_decl_list.size()):
            element.var_decl_list.element_at(index).accept_type(self)
    
        for index in range(element.method_decl_list.size()):
            element.method_decl_list.element_at(index).accept_type(self)
        
        return None

    def visit_var_decl(self, element: VarDecl) -> Type:
        element.type.accept_type(self)
        element.name.accept_type(self)
        return None
     

    def visit_method_decl(self, element: MethodDecl) -> Type:
        t = element.type.accept_type(self)
        element.name.accept_type(self)

        for index in range(element.formal_param_list.size()):
            element.formal_param_list.element_at(index).accept_type(self)

        for index in range(element.var_decl_list.size()):
            element.var_decl_list.element_at(index).accept_type(self)

        for index in range(element.statement_list.size()):
            element.statement_list.element_at(index).accept_type(self)
        if not type(t)==type(element.return_exp):
          self.add_semantic_error(SemanticErrorType.RETURN_TYPE_MISMATCH)
        element.return_exp.accept_type(self)
        return None


    def visit_formal(self, element: Formal) -> Type:
        element.type.accept_type(self)
        element.type.accept_type(self)
        return None


    def visit_int_array_type(self, element: IntArrayType) -> Type:
        return None
    
    def visit_boolean_type(self, element: BooleanType) -> Type:
        return None
    
    def visit_integer_type(self, element: IntegerType) -> Type:
        return None

    
    def visit_identifier_type(self, element: IdentifierType) -> Type:
        return None

    
    def visit_block(self, element: Block) -> Type:
        for index in range(element.statement_list.size()):
            element.statement_list.element_at(index).accept_type(self)
        
        return None

    def visit_if(self, element: If) -> Type:
        element.condition_exp.accept_type(self)
        element.if_statement.accept_type(self)
        element.else_statement.accept_type(self)
        return None
  

    def visit_while(self, element: While) -> Type:
        element.condition_exp.accept_type(self)
        element.statement.accept_type(self)
        return None

    
    def visit_print(self, element: Print) -> Type:
        element.print_exp.accept_type(self)
        return None


    def visit_assign(self, element: Assign) -> Type:
        left = element.left_side.accept_type(self)
        right = element.right_side.accept_type(self)
        if not type(right) is Type:
          self.add_semantic_error(SemanticErrorType.ASSIGN_TYPE_MISMATCH)
        return None

    
    def visit_array_assign(self, element: ArrayAssign) -> Type:
        element.array_name.accept_type(self)
        ls = element.array_exp.accept_type(self)
        rs = element.right_side.accept_type(self)
        if not type(ls) is Type or type(rs) is Type: 
          self.add_semantic_error(SemanticErrorType.ARRAY_ASSIGN_TYPE_MISMATCH)
        return None

    
    def visit_and(self, element: And) -> Type:
        left = element.left_side.accept_type(self)
        right = element.right_side.accept_type(self)
        if not self.checkTypes(left,right,BooleanType()):
            self.add_semantic_error(SemanticErrorType.AND_TYPE_MISMATCH)
        return BooleanType()

    def visit_less_than(self, element: LessThan) -> Type:
        left = element.left_side.accept_type(self)
        right = element.right_side.accept_type(self)
        if not self.checkTypes(left,right,IntegerType()):
            self.add_semantic_error(SemanticErrorType.LESS_THAN_TYPE_MISMATCH)
        return BooleanType()


    def visit_plus(self, element: Plus) -> Type:
        left = element.left_side.accept_type(self)
        right = element.right_side.accept_type(self)
        if not self.checkTypes(left,right,IntegerType()):
            self.add_semantic_error(SemanticErrorType.PLUS_TYPE_MISMATCH)
        return IntegerType()


    def visit_minus(self, element: Minus) -> Type:
        left = element.left_side.accept_type(self)
        right = element.right_side.accept_type(self)
        if not self.checkTypes(left,right,IntegerType()):
            self.add_semantic_error(SemanticErrorType.MINUS_TYPE_MISMATCH)
        return IntegerType()

    
    def visit_times(self, element: Times) -> Type:
        left = element.left_side.accept_type(self)
        right = element.right_side.accept_type(self)
        if not self.checkTypes(left,right,IntegerType()):
            self.add_semantic_error(SemanticErrorType.TIMES_TYPE_MISMATCH)
        return IntegerType()


    def visit_array_lookup(self, element: ArrayLookup) -> Type:
        left = element.out_side_exp.accept_type(self)
        right = element.in_side_exp.accept_type(self)
        if not type(left)==IntArrayType() :
          self.add_semantic_error(SemanticErrorType.ARRAY_TYPE_MISMATCH )
          
        
        if not type(right)==IntegerType():
          self.add_semantic_error(SemanticErrorType.INDEX_TYPE_MISMATCH )
        
        return None

    def visit_array_length(self, element: ArrayLength) -> Type:
        e = element.length_exp.accept_type(self)
        if not type(e) is IntArrayType():
          self.add_semantic_error(SemanticErrorType.ARRAY_LENGTH_TYPE_MISMATCH )
        return None


    def visit_call(self, element: Call) -> Type:
        element.callee_exp.accept_type(self)
        element.callee_name.accept_type(self)
        for index in range(element.arg_list.size()):
            if not type(arg_list.element_at(index)) == IdentifierType():
              self.add_semantic_error(SemanticErrorType.ARG_TYPE_MISMATCH)
            element.arg_list.element_at(index).accept_type(self)
        return None
    


    def visit_integer_literal(self, element: IntegerLiteral) -> Type:
        return None


    def visit_true_exp(self, element: TrueExp) -> Type:
        return BooleanType()


    def visit_false_exp(self, element: FalseExp) -> Type:
        return BooleanType()


    def visit_identifier_exp(self, element: IdentifierExp) -> Type:
        return None


    def visit_this(self, element: This) -> Type:
        return None


    def visit_new_array(self, element: NewArray) -> Type:
        e = element.new_exp.accept_type(self)
        if not type(e)==IntegerType():
           self.add_semantic_error(SemanticErrorType.NEW_ARRAY_TYPE_MISMATCH)
        
        return None


    def visit_new_object(self, element: NewObject) -> Type:
        element.object_name.accept_type(self)
        return None


    def visit_not(self, element: Not) -> Type:
        element.negated_exp.accept_type(self)
        return BooleanType()


    def visit_identifier(self, element: Identifier) -> Type:
        return None
