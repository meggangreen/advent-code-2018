 # reddit domm_plix did what I wanted to do
 # ... but his solution doesn't work for my input

use strict;
use warnings;
use 5.026;

my $in = join('',<>);

# remove circles
while ($in =~/\([^(]+\|\)/) {
    $in=~s/\([^(]+\|\)//g;
}
say "circles removed";

my %branches=(1=>[0,0]);
my $branch=1;
my $max=0;
foreach my $l (split(//,$in)) {
    if ($l=~/[NSEW]/) {
        $branches{$branch}->[0]++;
    }
    if ($l eq '(') {
        my $new_branch=$branch.'_1';
        # say "new branch $new_branch";
        my $val = $branches{$branch}->[0];
        $branches{$new_branch} = [ $val, $val];
        $branch = $new_branch;
    }
    elsif ($l eq ')') {
        # say "close branch $branch";
        $branch =~s/_\d+$//;
        # say "back on $branch";
    }
    elsif ($l eq '|') {
        my ($counter) = $branch =~ /_(\d+)$/;
        $counter++;
        my $new_branch = $branch;
        $new_branch=~s/(\d+)$/$counter/;
        # say "new branch $new_branch";
        my $val = $branches{$branch}->[1];
        $branches{$new_branch} = [ $val, $val];
        $branch = $new_branch;
    }
    $max = $branches{$branch}[0] if $max < $branches{$branch}[0];
}
say $max;