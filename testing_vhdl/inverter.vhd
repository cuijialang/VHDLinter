ENTITY inv IS
port (d : in bit;
      q :out bit);
END inv;

architecture inv_arc of inv is
begin
    process(d)
    begin
    q <= not d after 30ps; --XXX
    end process;
end inv_arc;
