# subroutine to implement insertion_sorting
#!/usr/bin/perl -w

use feature qw(say);

use Time::HiRes;

$t1 = Time::HiRes::time();

sub insertion_sort {
    my (@list) = @_;
    foreach my $i (1 .. $#list){
	    my $j = $i;
	    my $tmp = $list[$i];
    	while ($j >0 && $tmp < $list[$j-1]){
    		$list[$j] = $list[$j-1];
    		$j --;
		}
		$list[$j]=$tmp;

	}
	return @list;
}

my @tableau = ();
for (my $i = 0; $i <= 10000; $i++) {
    my $random_number = int(rand(100));
    push(@tableau, $random_number);
}

my @test = &insertion_sort(@tableau);

$t2 = Time::HiRes::time();

$t3 = $t2 - $t1;

say $t3;