entity my_entity is
port(
    out_1  : out std_logic;
    reg    : in std_logic_vector(0 to 7);
    data_in  : in bit
);
end entity my_entity;

architecture my_entity_arc of my_entity is
    subtype type_value is integer range 0 to 255;
    signal do : type_value := 0;
    signal internal_data_out_signal11 : std_logic vector(7 downto 0) := ”00000000”;

begin

    process_1 : process(data_in)
    begin
        if (data_in = '1') and (data_in'event) then
            if do < 254 then
                do <= do + 1;
            else
                do <= 0;
            end if;
        end if;
        internal_data_out_signal1 <=conv_std_logic_vector(do,8);
    end process;

    process_2 : process(internal_data_out_signal1, reg)
    begin
        if (internal_data_out_signal1 < reg) then
            out_1 <= '1';
        else
            out_1 <= '0';
        end if ;
end;
