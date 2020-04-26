entity and2 is
port (a,b : in std_ulogic;
        y : out std_ulogic);
end and2;

architecture behav of and2 is
begin
	y <= a and b;
end behav;
